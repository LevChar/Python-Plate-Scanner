class enteranceRules():

    @staticmethod
    def check_emergency_vehicles(plate):
        return True if (any(c.isalpha() for c in plate)) else False

    @staticmethod
    def sum_digits(plate):
        return sum(int(x) for x in plate if x.isdigit())

    @staticmethod
    def count_digits(plate):
        return sum(1 for x in plate if x.isdigit())

    @staticmethod
    def check_last_digits(case, plate):
        prohibited_last_digits_case1 = ("25", "26")
        prohibited_last_digits_case2 = ("85", "86", "87", "88", "89", "00")

        if case == 1:
            return True if plate.endswith(prohibited_last_digits_case1) else False
        else:
            return True if plate.endswith(prohibited_last_digits_case2) else False