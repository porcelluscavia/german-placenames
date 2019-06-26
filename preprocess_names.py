import pygeoj
import pandas as pd



class TextPrepper:
    def __init__(self, reg_set, kreise_set):
        self.reg_set = reg_set
        self.kreise_set = kreise_set
        #why did I write "pass" ?
        pass

    def read_file(self, geojson_path):
        """Return the all the fields from the geojson file."""

        geojson_tagset = pygeoj.load(geojson_path)
        return geojson_tagset

    def find_features_geojson(self, geojson_tagset):
        """Return list with kreis, regionsbezirk, and bundesland for each Kreis."""
        kreis_region_bund_list = []
        only_regs_set = set()
        for feature in geojson_tagset:
            bundesl = feature.properties.get('NAME_1')
            region = feature.properties.get('NAME_2')
            kreis = feature.properties.get('NAME_3')

            kreis_region_bund_list.append((kreis, region, bundesl))
        #Check: does "Göttingen" appear in this list as a region?
        return kreis_region_bund_list

    def make_krb_dataframe(self, kreis_region_bund):
        """Create kreis, regionsbezirk, and bundesland dataframe; Clean up Kreis names."""

        krb_df = pd.DataFrame(kreis_region_bund, columns=['Kreis', 'Region', 'Bundesland'])
        #TODO inspect, ensure no null values
        #inspected manually, found issues with kreis names
        krb_df['Kreis'].replace(to_replace=' Städte|-Kreis| Kreis| Land|Landkreis |Städteregion ', value ='', regex=True)

        return krb_df

    def ort_kreis_reader(self, csv_file):
        """Read in the Ort-Kreis csv file and clean up entries; Return Ort Kreis dataframe"""

        ort_kreis_df = pd.read_csv(csv_file, usecols=[1,3], columns=['Ort', 'Kreis'], skiprows=1)

        ort_kreis_df = ort_kreis_df.drop_duplicates(keep='first')
        # inspected manually, found issues with kreis names
        #cities kreis names are null, so fill their kreis slot with that city name
        ort_kreis_df[['Kreis']] = ort_kreis_df[['Kreis']].fillna(method='bfill', axis = 'columns')

        ort_kreis_df['Kreis'].replace(to_replace=' Städte|-Kreis| Kreis| Land|Landkreis |Städteregion ', value= '', regex=True)

        return ort_kreis_df

    def get_kreise_not_in_geojson(self, krb_df, ort_kreis_df, file_name):
        """Write a CSV file containing the entries from the Ort Kreis dataframe that could not be merged with the kreis, regionsbezirk, and bundesland (krb_df) dataframe.

            Attempts to merge Ort Kreis and krb dataframes on Kreis, but the some Kreis names are wriitten slighly differntly in the two dataframes.
            The Kreise from ort_kreis_df that have not been merged are written to a csv file for manual inspection.
        """

        merged = pd.merge(krb_df, ort_kreis_df, on='Kreis', how='right')
        #if Bundesland field is null, mismatch in kreis names in datasets
        unmerged_rows = merged[merged.Bundesland.isna()]
        missing_kreise_df = unmerged_rows['Kreis']
        missing_kreise_df.to_csv(file_name)
        return


    def map_new_kreise(self, krb_df, ort_kreis_df, csv_map_file):
        """Write a CSV file containing the entries from the Ort Kreis dataframe that could not be merged with the kreis, regionsbezirk, and bundesland (krb_df) dataframe

                    Attempts to merge Ort Kreis and krb dataframes on Kreis, but the some Kreis names are wriitten slighly differntly in the two dataframes.
                    The Kreise from ort_kreis_df that have not been merged are written to a csv file for manual inspection
        """
        kreis_jsonkreis_map = read_csv(csv_map_file)
        #TODO change the name on krb_df's kreise
        #TODO merge krb_df and ort_kreis_df inner join on kreis, check that it all goes through


    #TODO now that we have a fully merged dataframe, with ort,kreise,region, and bundesland, we can make a trie
    #TODO  find best way to get text out of ort for each name, set up formulae such as percentage/all, regionsbezirk with most of that ending
    #TODO find how to make the geojson visual, how to make it interactive, how to make it communicate with backend







if '__main__' == __name__:

    reg_set = []
    kreise_set = []

    path = "/Users/samski/PycharmProjects/geo/landkreise.geojson"
    csv_path_3 = "/Users/samski/PycharmProjects/geo/zuordnung_plz_ort_landkreis.csv"

    new_reader = TextPrepper(reg_set, kreise_set)

    landkreise_geo_file = new_reader.read_file(path)
    landkreise_list = new_reader.find_features_reg(landkreise_geo_file)

    #column_names= ['ort','kreis']