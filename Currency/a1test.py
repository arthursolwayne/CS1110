"""
Test script for module a1

When run as a script, this module invokes several procedures that 
test the various functions in the module a1.

Author: Arthur Wayne asw263
Date:   30 September 2020
"""
import a1
import introcs

def testA():
    """
    Test procedure for Part A
    """

    #tests space at beginning of string for before_space 
    introcs.assert_equals("", a1.before_space(" my name"))
    #tests space at beginning of string for after_space
    introcs.assert_equals("my name", a1.after_space(" my name"))

    #tests space in between words of string for before_space
    introcs.assert_equals("my", a1.before_space("my name"))
    #tests space in between words of string for after_space
    introcs.assert_equals("name", a1.after_space("my name"))

    #tests multiple spaces in between words of string for before_space
    introcs.assert_equals("my", a1.before_space("my name is Arthur"))
    #tests multiple spaces in between words of string for after_space
    introcs.assert_equals("name is Arthur", a1.after_space("my name is Arthur"))

    #tests single space as the string for before_space
    introcs.assert_equals("", a1.before_space(" "))
    #tests single space as the string for after_space 
    introcs.assert_equals("", a1.after_space(" ")) 

    #tests an empty string as the string for before_space
    introcs.assert_equals("", a1.before_space(""))
    #tests an empty string as the string for after_space 
    introcs.assert_equals("", a1.after_space("")) 

def testB():
    """
    Test procedure for Part B
    """
    
    #sample json to test functions of part B
    test_json = '{ "src":"2 Namibian Dollars", "dst":"2 Lesotho Maloti", "valid":true, "err":"" }'

    #tests get_src
    a1.get_src(test_json)

    #tests get_dst
    a1.get_dst(test_json)

    #tests has_error
    a1.has_error(test_json)

    #tests has_error with false in valid field
    test_json_false = '{ "src":"2 Namibian Dollars", "dst":"2 Lesotho Maloti", "valid":false, "err":"" }'
    a1.has_error(test_json_false)
    
    #PRODUCES ERROR
    #tests blank json for all functions
    #blank_json = ''
    #a1.get_src(blank_json)
    #a1.get_src(blank_json)
    #a1.get_src(blank_json)

def testC():
    """
    Test procedure for Part C
    """
    
    #tests currency_response with 5.6 USD to CAD 
    a1.currency_response('USD', 'CAD', 5.6)

    #tests currency_response with invalid from value
    a1.currency_response('UDSER', 'CAD', 5.6)

    #tests currency_response with invalid from value
    a1.currency_response('UDS', 'CDAER', 5.6)

    #tests currency_response with an int amt value
    a1.currency_response('UDS', 'CDA', 5)

    #PRODUCES ERROR
    #tests currency_response with no arguments
    #a1.currency_response()

def testD():
    """
    Test procedure for Part D
    """

    #test is_currency with CAD
    a1.is_currency('CAD')
    #test is_currency with blank field
    a1.is_currency('')
    #test is_currency with invalid currency
    a1.is_currency('CADA')    

    #tests exchange with 5.6 USD to CAD 
    a1.exchange('USD', 'CAD', 5.6)
    #tests exchange with invalid from value
    a1.exchange('UDSER', 'CAD', 5.6)
    #tests exchange with invalid from value
    a1.exchange('UDS', 'CDAER', 5.6)
    #tests exchange with an int amt value
    a1.exchange('UDS', 'CDA', 5)

testA()
testB()
testC()
testD()
print('Module a1 passed all tests.')
