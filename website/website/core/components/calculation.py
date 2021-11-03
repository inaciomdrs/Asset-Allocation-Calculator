from django_unicorn.components import UnicornView, UnicornField


class Asset(UnicornField):
    def __init__(self, name="", percentage=0):
        self.name = name
        self.percentage = percentage


class CalculationView(UnicornView):
    name = "Calculation"
    input_data = None
    data = []

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs) 
        self.name = kwargs.get("name", "Calculation")

    def _split_lines(self):
        return self.input_data.split("\n")

    def _build_asset_from(self, line):
        asset, percentage = line.split(",")
        return Asset(asset, int(percentage))

    def _build_assets(self, lines):
        self.data = [
            self._build_asset_from(line)
            for line in lines
        ]

    def calculate(self):
        self.data = []
        self._build_assets(self._split_lines())
