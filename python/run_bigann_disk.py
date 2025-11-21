import subprocess
from pathlib import Path


BASE_DIR = Path.home() / "projects" / "aisaq-diskann"
BUILD_DIR = BASE_DIR / "build"


def run(cmd):
    print("> " + " ".join(cmd))
    subprocess.run(cmd, cwd=BUILD_DIR, check=True)


def main() -> None:
    build_cmd = [
        "./apps/build_disk_index",
        "--data_type",
        "float",
        "--dist_fn",
        "l2",
        "--data_path",
        "data/sift/sift_learn.fbin",
        "--index_path_prefix",
        "data/sift/disk_index_sift_learn_R32_L50_A1.2",
        "-R",
        "32",
        "-L",
        "50",
        "-B",
        "0.003",
        "-M",
        "1",
    ]
    search_cmd = [
        "./apps/search_disk_index",
        "--data_type",
        "float",
        "--dist_fn",
        "l2",
        "--index_path_prefix",
        "data/sift/disk_index_sift_learn_R32_L50_A1.2",
        "--query_file",
        "data/sift/sift_query.fbin",
        "--gt_file",
        "data/sift/sift_query_learn_gt100",
        "-K",
        "10",
        "-W",
        "2",
        "-L",
        "10",
        "20",
        "40",
        "--result_path",
        "data/sift/res",
        "--num_nodes_to_cache",
        "10000",
    ]

    run(build_cmd)
    run(search_cmd)


if __name__ == "__main__":
    main()

