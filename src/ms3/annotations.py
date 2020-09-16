import pandas as pd

from .utils import load_tsv, decode_harmonies
from .logger import get_logger

class Annotations:

    def __init__(self, tsv_path=None, df=None, index_col=None, sep='\t', logger_name='Harmonies', level=None):
        self.logger = get_logger(logger_name, level)
        if df is not None:
            self.df = df
        else:
            assert tsv_path is not None, "Name a TSV file to be loaded."
            self.df = load_tsv(tsv_path, index_col=index_col, sep=sep)


    def __repr__(self):
        layers = [col for col in ['staff', 'voice', 'harmony_type'] if col in self.df.columns]
        return f"{len(self.df)} labels:\n{self.df.groupby(layers).size().to_string()}"


    def get_labels(self, staff=None, voice=None, harmony_type=None, positioning=False, decode=False):
        """ Returns a list of harmony tags from the parsed score.

        Parameters
        ----------
        staff : :obj:`int`, optional
            Select harmonies from a given staff only. Pass `staff=1` for the upper staff.
        harmony_type : {0, 1, 2}, optional
            If MuseScore's harmony feature has been used, you can filter harmony types by passing
                0 for 'normal' chord labels only
                1 for Roman Numeral Analysis
                2 for Nashville Numbers
        positioning : :obj:`bool`, optional
            Set to True if you want to include information about how labels have been manually positioned.
        decode : :obj:`bool`, optional
            Set to True if you don't want to keep labels in their original form as encoded by MuseScore (with root and
            bass as TPC (tonal pitch class) where C = 14).

        Returns
        -------

        """
        sel = pd.Series(True, index=self.df.index)
        if staff is not None:
            sel = sel & (self.df.staff == staff)
        if voice is not None:
            sel = sel & (self.df.voice == voice)
        if harmony_type is not None and 'harmony_type' in self.df.columns:
            sel = sel & (self.df.harmony_type == harmony_type)
            # if the column contains strings and NaN:
            # (pd.to_numeric(self.df['harmony_type']).astype('Int64') == harmony_type).fillna(False)
        res = self.df[sel]
        if decode:
            res = decode_harmonies(res)
        if positioning:
            pass # TODO
        return res