import argparse
from pathlib import Path
import shutil
import subprocess

# scannet_path = Path("data/scannet")
# noisy_scannet_path = Path("data/scannet")

def clean(args):
    scannet_path = Path("data/scannet")
    paths = [
        scannet_path / Path("__pycache__"),
        scannet_path / Path("instance_mask"),
        scannet_path / Path("points"),
        scannet_path / Path("scannet_instance_data"),
        scannet_path / Path("semantic_mask"),
        scannet_path / Path("super_points"),
    ]

    for path in paths:
        print(f"removing {str(path)}")
        shutil.rmtree(path, ignore_errors=True)
    
    for pickle in scannet_path.glob("*.pkl"):
        print(f"removing {pickle}")
        pickle.unlink(missing_ok=True)
    
def copy_noisy_scannet_test(args):

    scannet_path = Path("../../data/scannet")
    noisy_scannet_path = Path("../../data/noisy_downs_scannet")

    with open(Path("data/scannet") / "meta_data/scannetv2_val.txt", 'r') as f:
        for scan in f.readlines():
            scan_string = scan.strip()
            scan_path = scannet_path / "scans" / scan_string
            noisy_scan_path = noisy_scannet_path / "scans" / scan_string

            noisy_scan_path.mkdir(parents=True, exist_ok=True)
            files = [
                ".aggregation.json",
                ".txt",
                "_2d-instance.zip",
                "_2d-instance-filt.zip",
                "_2d-label.zip",
                "_2d-label-filt.zip",
                "_vh_clean.aggregation.json",
                "_vh_clean.ply",
                "_vh_clean.segs.json",
                "_vh_clean_2.labels.ply",
                "_vh_clean_2.0.010000.segs.json",
            ]

            point_clouds = [
                "_vh_clean.ply",
                "_vh_clean_2.ply",
            ]

            for file in files:
                shutil.copy(scan_path / f"{scan_string}{file}", noisy_scan_path)
            
            shutil.copy2(scan_path / f"{scan_string}_scan_downs.ply", noisy_scan_path / f"{scan_string}_vh_clean_2.ply")


def preprocess(args):
    scannet_path = Path("data/scannet")
    subprocess.run(["python", "batch_load_scannet_data.py"], 
                   cwd=scannet_path, 
                   check=True)

    subprocess.run([
        "python", "tools/create_data.py", 
        "scannet", 
        "--root-path", "./data/scannet", 
        "--out-dir", "./data/scannet", 
        "--extra-tag", "scannet"
    ], cwd=".", check=True)

def test(args):
    subprocess.run([
        "python", "tools/test.py", 
        "configs/oneformer3d_1xb4_scannet.py", 
        "work_dirs/pretrained/oneformer3d_1xb4_scannet.pth"
        ], cwd=".", check=True)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    cleaner = subparsers.add_parser("clean")
    cleaner.set_defaults(func=clean)

    copier = subparsers.add_parser("copy")
    copier.set_defaults(func=copy_noisy_scannet_test)

    preprocessor = subparsers.add_parser("preprocess")
    preprocessor.set_defaults(func=preprocess)

    tester = subparsers.add_parser("test")
    tester.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()