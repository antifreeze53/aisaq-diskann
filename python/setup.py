import subprocess
import pathlib

base = pathlib.Path.home() / "projects" / "aisaq-diskann"
build_dir = base / "build"
data_dir = build_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

def run(cmd, cwd=build_dir):
    print("> " + " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

tarball = data_dir / "sift.tar.gz"
if not tarball.exists():
    run(["wget", "ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz"], cwd=data_dir)

sift_dir = data_dir / "sift"
if not (sift_dir / "sift_learn.fvecs").exists():
    run(["tar", "-xf", "sift.tar.gz"], cwd=data_dir)

learn_bin = sift_dir / "sift_learn.fbin"
query_bin = sift_dir / "sift_query.fbin"
if not learn_bin.exists():
    run(["./apps/utils/fvecs_to_bin", "float", "data/sift/sift_learn.fvecs", "data/sift/sift_learn.fbin"])
if not query_bin.exists():
    run(["./apps/utils/fvecs_to_bin", "float", "data/sift/sift_query.fvecs", "data/sift/sift_query.fbin"])

gt_file = sift_dir / "sift_query_learn_gt100"
if not gt_file.exists():
    run([
        "./apps/utils/compute_groundtruth",
        "--data_type", "float",
        "--dist_fn", "l2",
        "--base_file", "data/sift/sift_learn.fbin",
        "--query_file", "data/sift/sift_query.fbin",
        "--gt_file", "data/sift/sift_query_learn_gt100",
        "--K", "100",
    ])
