import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_feasibility_plots(file_path):
    df = pd.read_csv(
        file_path,
        sep=r"\s*\|\s*", 
        engine="python",
        skipfooter=2, 
    )

    df.columns = [col.strip() for col in df.columns]

    df["feasible(true)"] = df["feasible(true)"].astype(str).str.strip().str.upper()
    df["stl_temp"] = pd.to_numeric(df["stl_temp"], errors="coerce")
    df["iters"] = pd.to_numeric(df["iters"], errors="coerce")

    df = df.dropna(subset=["stl_temp", "iters", "feasible(true)"])

    df["is_feasible"] = df["feasible(true)"].apply(
        lambda x: 0 if x == "YES" else 1
    )

    temperatures = df["stl_temp"].unique()

    for temp in temperatures:
        temp_data = (
            df[df["stl_temp"] == temp]
            .sort_values("iters")
            .reset_index(drop=True)
        )

        iterations = temp_data["iters"].values
        feasibility_colors = temp_data["is_feasible"].values

        grid_data = np.expand_dims(feasibility_colors, axis=0)

        fig, ax = plt.subplots(figsize=(10, 1.5))

        cax = ax.imshow(
            grid_data,
            cmap="gray",
            aspect="auto",
            vmin=0,
            vmax=1,
            extent=[
                iterations[0] - 5,
                iterations[-1] + 5,
                0,
                1,
            ], 
        )

        ax.set_yticks([]) 
        ax.set_xticks(iterations)
        ax.set_xlabel("Iterations", fontsize=10)
        ax.set_title(
            f"Feasibility Plot (Temperature = {temp})",
            fontsize=12,
            fontweight="bold",
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(
            f"feasibility_temp_{temp}.png", dpi=300, bbox_inches="tight"
        )
        plt.show()

if __name__ == "__main__":
    generate_feasibility_plots("/home/xlab/rao/stl-svpio/data/table1.txt")