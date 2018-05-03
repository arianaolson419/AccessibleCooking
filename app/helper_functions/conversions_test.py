import conversions

def _test_fractional_replacement(original_str, expected_str):
    pass

def fractional_replacement_test_no_op():
    original_str = "2 cups of cornmeal"
    expected_str = "2 cups of cornmeal"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "One fourth stick of butter"
    expected_str = "One fourth stick of butter"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "Stir in 1 and a third cups of chocolate chips"
    expected_str = "Stir in 1 and a third cups of chocolate chips"
    _test_fractional_replacement(original_str, expected_str)

def fractional_replacement_test_slash():
    original_str = "1/3 cup of flour"
    expected_str = "One third cup of flour"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "2 2/3 cups of sugar"
    expected_str = "Two and two third cups of sugar"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "Sift in the 1/4 cup of cocoa powder"
    expected_str = "Sift in the one quarter cup of cocoa powder"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "Heat up 2 3/4 cups of oil"
    expected_str = "Heat up two and three quarters cups of oil"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "One stick (1/2 cup) of butter"
    expected_str = "One stick (half cup) of butter"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "1 1/8 cup of milk"
    expected_str = "One and one eighth cup of milk"
    _test_fractional_replacement(original_str, expected_str)

def fractional_replacement_test_unicode():
    original_str = "⅓ cup of flour"
    expected_str = "One third cup of flour"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "2⅔ cups of sugar"
    expected_str = "Two and two third cups of sugar"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "Sift in the ¼ cup of cocoa powder"
    expected_str = "Sift in the one quarter cup of cocoa powder"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "Heat up 2 ¾ cups of oil"
    expected_str = "Heat up two and three quarters cups of oil"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "One stick (½ cup) of butter"
    expected_str = "One stick (half cup) of butter"
    _test_fractional_replacement(original_str, expected_str)

    original_str = "1⅛ cup of milk"
    expected_str = "One and one eighth cup of milk"
    _test_fractional_replacement(original_str, expected_str)

if __name__ == '__main__':
    fractional_replacement_test_no_op()
    fractional_replacement_test_slash()
    fractional_replacement_test_unicode()