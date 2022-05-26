import argparse

import pandas as pd

from producers.BaseProducer import BaseProducer


class IceSheetsProducer(BaseProducer):

    def load_dataset(self):
        return self.load_sea_ice_extent()

    def load_sea_ice_extent(self):
        print("loading data...")
        # could be swapped to streaming from disk. Then, without using pandas
        df_north = pd.read_csv(f"{self.data_source.rstrip('/')}/N_seaice_extent_daily_v3.0.csv")
        df_north = df_north.drop(0)
        df_north["Hemisphere"] = "N"
        df_south = pd.read_csv(f"{self.data_source.rstrip('/')}/S_seaice_extent_daily_v3.0.csv")
        df_south = df_south.drop(0)
        df_south["Hemisphere"] = "S"

        df_combined = pd.concat([df_north, df_south], axis=0).reset_index(drop=True)
        df_combined.columns = [c.strip() for c in df_combined.columns]

        for c in ['Year', 'Month', 'Day', 'Extent', 'Missing']:
            df_combined[c] = pd.to_numeric(df_combined[c])

        df_combined = df_combined.drop(["Source Data"], axis=1)
        df_combined = df_combined.sort_values(['Year', 'Month', 'Day'])
        print("data loading complete")

        self.key = "Hemisphere"
        return df_combined


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data streaming utility for sending climate datasets to kafka")
    parser.add_argument("-d", "--input_dir", help="directory to where to find the data")

    args = parser.parse_args()

    producer = IceSheetsProducer(args.input_dir)
    producer.streaming_loop()
