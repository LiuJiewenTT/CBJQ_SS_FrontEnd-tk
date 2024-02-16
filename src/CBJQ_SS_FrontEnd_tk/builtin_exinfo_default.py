class Builtin_ExInfo:
    edition_parts = [None, None, None]
    edition_str = 'Not Built'
    build_timestamp = 0
    build_timestamp_str = 'Never'
    program_iconpicture_idx = None
    hasSplash = False

    def summary_str_multiline(self):
        retv = f'Edition: {self.edition_str}\nBuild Timestamp: {self.build_timestamp_str}\n'
        return retv

    def summary_str_singleline(self):
        retv = f'Build Info: {self.edition_str} [{self.build_timestamp_str}]'
        return retv

