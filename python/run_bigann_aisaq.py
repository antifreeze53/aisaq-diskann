import subprocess
from pathlib import Path


BASE_DIR = Path.home() / "projects" / "aisaq-diskann"
BUILD_DIR = BASE_DIR / "build"


def run(cmd):
    print("> " + " ".join(cmd))
    subprocess.run(cmd, cwd=BUILD_DIR, check=True)


def main():
    build_cmd = [
        "./apps/build_disk_index",
        "--data_type",
        "float",
        "--dist_fn",
        "l2",
        "--data_path",
        "data/sift/sift_learn.fbin",
        "--index_path_prefix",
        "data/sift/aisaq_disk_index_R64_L125_B1_M128",
        "-R",
        "64",
        "-L",
        "125",
        "-B",
        "1",
        "-M",
        "128",
        "--QD",
        "32",
        "--use_aisaq",
        "--inline_pq",
        "32",
        "--rearrange",
    ]
    search_cmd = [
        "./apps/search_disk_index",
        "--data_type",
        "float",
        "--dist_fn",
        "l2",
        "--index_path_prefix",
        "data/sift/aisaq_disk_index_R64_L125_B1_M128",
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
        # "-T",
        # "8",
        "--use_aisaq",
        # "-V",
        # "2",
        "--pq_cache_size",
        "100",
        "--result_path",
        "data/sift/res_aisaq",
    ]
    run(build_cmd)
    run(search_cmd)


if __name__ == "__main__":
    main()

