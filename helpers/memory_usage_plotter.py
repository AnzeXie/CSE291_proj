import matplotlib.pyplot as plt
from pathlib import Path
import os

def pass_data(dir, name):
    # to_do_list = ["blur_i.out", "dot_map_i.out", "detect_edges_i.out", "gray_scale_i.out"]
    # to_do_list = ["blur_ms.out", "dot_map_ms.out", "detect_edges_ms.out", "gray_scale_ms.out"]

    # to_do_list = ["blur_i.out", "dot_map_i.out", "detect_edges_i.out", "gray_scale_i.out", 
    #                 "obj_recog_i.out"]
    to_do_list = ["blur_ms.out", "dot_map_ms.out", "detect_edges_ms.out", "gray_scale_ms.out",
                    "obj_recog_ms.out"]

    # to_do_list = ["blur_agg_ms.out", "dot_map_agg_ms.out", "detect_edges_agg_ms.out", "gray_scale_agg_ms.out",
    #                 "obj_recog_agg_ms.out"]

    # to_do_list = ["gray_scale_agg_ms.out"]


    for file in os.listdir(dir):
        if Path(file).suffix != ".out":
            continue
        if Path(file).name not in to_do_list:
            continue
        f = open(Path(dir) / Path(file), 'r')    
        time = []
        mem = []
        for l in f.readlines():
            if "time=" in l:
                time.append(int(l.split('=')[1]))
            if "mem_heap_B" in l:
                mem.append(int(l.split('=')[1]) / (10**6))

        time_0 = [i - time[0] for i in time]
        plt.plot(time_0, mem, label=Path(file).stem)
    
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(loc='upper left')
    plt.title("Memory usage (disaggregated version)")
    
    if name[-1] == "i":
        plt.xlabel('number of instructions')
    else:
        plt.xlabel('time (ms)')
    plt.ylabel('memory usage(MB)')
    plt.savefig(f"./log_img/{name}.png")
        




def main():
    # pass_data("./CSE291_proj/", "massif.out.9363")
    pass_data("./mem_log1/", "all_ops_ms.png")
    

if __name__ == "__main__":
    main()