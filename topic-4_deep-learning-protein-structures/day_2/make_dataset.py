from __future__ import annotations
from pathlib import Path
from pinder.core.index.system import PinderSystem
from pinder.core.loader import filters
from pinder.core import PinderLoader
from multiprocessing import Pool
from tqdm import tqdm
import pandas as pd

def select_ids(max_per_cluster=2, max_length=1024, max_length_per_monomer=512, min_length_per_monomer=50):
    base_filters = [
        filters.FilterByMissingHolo(),
        filters.FilterSubByContacts(min_contacts=5, radius=10.0, calpha_only=True),
        filters.FilterDetachedHolo(radius=12, max_components=2),
    ]
    sub_filters = [
        filters.FilterSubByAtomTypes(min_atom_types=4),
        filters.FilterByHoloOverlap(min_overlap=5),
        filters.FilterByHoloSeqIdentity(min_sequence_identity=0.8),
        filters.FilterSubRmsds(rmsd_cutoff=7.5),
        filters.FilterDetachedSub(radius=12, max_components=2),
    ]
    split_ids = {}
    for split in ["train", "val", "test"]:
        loader = PinderLoader(
            split=split,
            monomer_priority="pred",
            base_filters=base_filters,
            sub_filters=sub_filters,
        )
        index = loader.index.merge(loader.metadata, on="id", how="left")
        index["length"] = index["length1"] + index["length2"]
        index["resolution"] = index["resolution"].astype("float32")
        index = index[
            (index["length"] <= max_length)
            & (index["length1"] <= max_length_per_monomer)
            & (index["length2"] <= max_length_per_monomer)
            & (index["length1"] >= min_length_per_monomer)
            & (index["length2"] >= min_length_per_monomer)
            & (index["label"] == "BIO")
            & (index["method"] == "X-RAY DIFFRACTION")
            & (index.cluster_id_L != index.cluster_id_R)
            & (index.uniprot_R != index.uniprot_L)
            & (~(index.ECOD_names_R.str.split(",").apply(set) & index.ECOD_names_L.str.split(",").apply(set)).astype(bool))
        ].reset_index(drop=True)
        ids = list(
            set(
                index.sort_values(
                    ["resolution", "id"],
                    ascending=[True, True],
                )
                .groupby("cluster_id")
                .head(max_per_cluster)["id"]
            )
        )
        split_ids[split] = ids
    return split_ids


def save_system(system, folder: Path):
    row = {
        "pinder_id": system.native.pinder_id,
    }
    system_folder = folder / system.native.pinder_id
    system_folder.mkdir(parents=True, exist_ok=True)
    chain1_struc = system.holo_receptor
    chain1_struc.filter("element", mask=["H"], negate=True, copy=False)
    chain2_struc = system.holo_ligand
    chain2_struc.filter("element", mask=["H"], negate=True, copy=False)
    chain12_struc = system.create_complex(
        receptor=chain1_struc,
        ligand=chain2_struc,
        renumber_residues=True,
        remove_differing_atoms=True,
    )
    chain12_struc.to_pdb(system_folder / f"{chain12_struc.pinder_id}.pdb")
    chain1_struc = system.pred_receptor
    if chain1_struc is None:
        return row
    chain1_struc.filter("element", mask=["H"], negate=True, copy=False)
    chain2_struc = system.pred_ligand
    if chain2_struc is None:
        return row
    chain2_struc.filter("element", mask=["H"], negate=True, copy=False)
    chain12_struc_pred = system.create_complex(
        receptor=chain1_struc,
        ligand=chain2_struc,
        renumber_residues=True,
        remove_differing_atoms=True,
    )
    row["pred_pinder_id"] = chain12_struc_pred.pinder_id
    chain12_struc_pred.to_pdb(system_folder / f"{chain12_struc_pred.pinder_id}.pdb")
    return row

def process_id(args):
    id, key, data_dir = args
    system = PinderSystem(id)
    row = save_system(system, data_dir / key)
    row["split"] = key
    return row


def main():
    split_ids = select_ids()
    data_dir = Path("hackathon_data")
    data_dir.mkdir(parents=True, exist_ok=True)
    tasks = [(id, key, data_dir) for key in split_ids for id in split_ids[key]]

    with Pool(20) as pool:
        rows = list(tqdm(pool.imap(process_id, tasks), total=len(tasks)))
    df = pd.DataFrame(rows)
    df.to_csv("hackathon_data/data.csv", index=False)

if __name__ == "__main__":
    main()