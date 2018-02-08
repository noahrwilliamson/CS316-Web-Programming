#!/usr/bin/ruby

# Author: Noah Williamson
# CS316 Project 1

require 'cgi'

cgi = CGI.new("html5") # instantiate a new CGI obj w/ html5 default
ORIG_UNITS = cgi["origunits"].to_s # store our four GET parameters
NEW_UNITS = cgi["convunits"].to_s
NUM_UNITS = cgi["numunits"].to_f
CONV_FACTOR = cgi["convfactor"].to_f

UNIT_DATA = 
 %w[ parsec lightyear kilometer xlarn  galacticyear terrestrialyear xarnyear
    terrestrialminute ] # array containing valid units

CONV_DATA =
  { "parseclightyear" => 3.26, "lightyearparsec" => 0.30675,
    "lightyearkilometer" => 3.086 * 10**13, 
    "kilometerlightyear" => 3.086 * 10**-13,
    "xlarnparsec" => 7.3672, "parsecxlarn" => 0.13574,
    "galacticyearterrestrialyear" => 250_000_000.0,
    "terrestrialyeargalacticyear" => 4 * 10**-9,
    "xarnyearterrestrialyear" => 1.2579, "terrestrialyearxarnyear" => 0.79498,
    "terrestrialyearterrestrialminute" => 525600,
    "terrestrialminuteterrestrialyear" => 1.9026 * 10**-6 } # hash containing conversions
CONV_DATA.default = -1 # set default value to check against

ORIG_UNITS = ORIG_UNITS.downcase
NEW_UNITS = NEW_UNITS.downcase # we will ignore case for these purposes
ORIG_UNITS = ORIG_UNITS.delete(' ') # also be nice in case user enters a space
NEW_UNITS = NEW_UNITS.delete(' ')     # trailing/leading, also ex "light year" 

CONV_KEY = (ORIG_UNITS + NEW_UNITS) # our conversion key for our hash

# function to check input
def check_input
  if(( (CONV_DATA[CONV_KEY] != -1) || (ORIG_UNITS.eql?(NEW_UNITS) && 
        UNIT_DATA.include?(ORIG_UNITS) )  ) && NUM_UNITS != 0 && CONV_FACTOR != 0)
    _valid = true   # input is valid if we know what to do with all four params
  else
    _valid = false
  end
end

# function to compute result
def convert
  if(ORIG_UNITS.eql? NEW_UNITS)
    _result = NUM_UNITS * CONV_FACTOR  # treat as special case
  else
    _result = CONV_DATA[CONV_KEY] * NUM_UNITS * CONV_FACTOR
  end
end

# function to write CSS for invalid output
def format_invalid(info)
  i = 0
  output = ""
  while i < info.length
  if(!info[i])
      i += 1
      head_num = i.to_s
      head = "h" + head_num
      output += (head + "{color:red; font-weight:normal; font-size:16px} ")
    else
      i += 1
      head_num = i.to_s
      head = "h" + head_num
      output += (head + "{color:blue; font-weight:normal;  font-size:16px} ")
    end
  end
  return output
end

valid = check_input # validate input

# proceeding with the final result or error msg
if valid
  result = convert
  NUM_UNITS = NUM_UNITS.to_s
  CONV_FACTOR = CONV_FACTOR.to_s
  result = result.to_s
  
  # output params & result
  cgi.out{
    cgi.html{
      cgi.head{ cgi.title{"Result"} + 
        cgi.style('type' => 'text/css'){
          "h1{color:blue; font-weight:normal; font-size:16px}" +  
                "h2{color:green; font-weight:normal; font-size:16px}"
        }
      } +
      cgi.body{
        cgi.h1{
          "Original units: " + ORIG_UNITS  + cgi.br +
          "New units: " + NEW_UNITS + cgi.br + 
          "Amount of original units: " + NUM_UNITS + cgi.br +
          "Conversion factor: " + CONV_FACTOR + cgi.br + cgi.br
        } +
        cgi.h2{
          "Result: " + result + cgi.br
        }
      }
    }
  }
else
  valid_params = Array.new(4, false) # assume all are invalid
  if UNIT_DATA.include? ORIG_UNITS    # then decide which are valid (if any)
    valid_params[0] = true
  end
  if UNIT_DATA.include? NEW_UNITS
    valid_params[1] = true
  end
  if NUM_UNITS != 0
    valid_params[2] = true
  end
  if CONV_FACTOR != 0
    valid_params[3] = true
  end
  if CONV_DATA[CONV_KEY] != -1  # we have to check if we know how to convert the units!
    valid_params[0] = true        # i.e. in case user enters parsec and kilometer, both
    valid_params[1] = true          # valid but we can't do that conversion.
  end
  
  error_css = format_invalid valid_params    # get style info for error msg
  error_css += " p{color:red; font-weight:bold}" # make our p tag red and bold too

  # output error msg
  cgi.out{
    cgi.html{
      cgi.head{ cgi.title{"Error"} +
        cgi.style('type' => 'text/css'){
          error_css
        }
      } +
      cgi.body{
        cgi.h1{
          "Original units: " + ORIG_UNITS
        } +
        cgi.h2{
          "New units: " + NEW_UNITS
        } +
        cgi.h3{
          "Amount of original units: " + NUM_UNITS.to_s
        } +
        cgi.h4{
          "Conversion factor: " + CONV_FACTOR.to_s + cgi.br + cgi.br
        } + 
        cgi.p{
          "The parameters listed above in red are invalid or I do not know " +
          "how to do that conversion! Be sure to use a valid conversion!"
        }
      }
    }
  }
end

