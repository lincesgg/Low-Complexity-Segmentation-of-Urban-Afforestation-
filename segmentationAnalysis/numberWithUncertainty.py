import numpy as np
import re

class numberWithUncertainty:

    def __init__(self, value, uncertainty=0.0):
        self.value = value
        self.uncertainty = abs(uncertainty)
        
        
    @staticmethod
    def from_str(uncertainty_str:str):
        splitted_at_uncertaity: list[str] = uncertainty_str.split("±")
        
        for idx in range(len(splitted_at_uncertaity) - 1, -1, -1):
            crr_uncertainty = float(splitted_at_uncertaity[idx])
            respective_val = float(splitted_at_uncertaity[idx - 1])
            
            number_w_uncertainty = numberWithUncertainty(respective_val, crr_uncertainty)
            
            if (idx > 1):
                del splitted_at_uncertaity[idx]
                splitted_at_uncertaity[idx - 1] = number_w_uncertainty
            else:
                return number_w_uncertainty
        
        
    def became_copy_of(self, anotherNumber):
        self.value = anotherNumber.value
        self.uncertainty = anotherNumber.uncertainty

    # Private Uncertainty Arithmetic Operations ----
    INTERNAL_ALLOWED_OPERATIONS = ["+", "-", "*", "/"]
    INTERNAL_ALLOWED_COMPARASIONS = [">", "<", ">=", "<=", "==", "!="]
    
    def _sum_subtraction(self, anotherNumber, operator="+"):
        val_result = eval(f"{self.value} {operator} {anotherNumber.value}")
        uncertainty_result = self.uncertainty + anotherNumber.uncertainty
        
        return numberWithUncertainty(val_result, uncertainty_result)

    def _division_multiplication(self, anotherNumber, operator="*"):
        val_result = eval(f"{self.value} {operator} {anotherNumber.value}")
        uncertainty_result = val_result * ( (self.uncertainty / self.value) + (anotherNumber.uncertainty / anotherNumber.value) )
        
        return numberWithUncertainty(val_result, uncertainty_result)
    
    def _guarantee_number_w_uncertainty(self, anotherNumber):
        anotherNumber_type = type(anotherNumber)
        
        if anotherNumber_type != numberWithUncertainty:
            if not (anotherNumber_type in [int, float] or issubclass(anotherNumber_type, np.number)) and (not str(anotherNumber).replace(".","").replace("-", "").replace("e", "").isdigit()):
                raise TypeError(f"Mathematical Operation with <{type(self).__name__}> done with NAN value <{anotherNumber_type.__name__}>")
            
            elif anotherNumber_type != numberWithUncertainty:
                anotherNumber = numberWithUncertainty(anotherNumber, 0.0)
            
        return anotherNumber
    
    def _internal_arithmetic_operation(self, anotherNumber, operator="+|-|*|/"):
        assert (operator in self.INTERNAL_ALLOWED_OPERATIONS), f"Operator should be an internal allowed operator: {self.INTERNAL_ALLOWED_OPERATIONS}"
        
        anotherNumber = self._guarantee_number_w_uncertainty(anotherNumber)
            
        if operator in ['+', '-']:
            return self._sum_subtraction(anotherNumber, operator)
            
        elif operator in ['*', '/']:
            return self._division_multiplication(anotherNumber, operator)
        
        
    # Arithmetic Magic Methods ----

    def __add__(self, anotherNumber):
        return self._internal_arithmetic_operation(anotherNumber, "+")

    def __sub__(self, anotherNumber):
        return self._internal_arithmetic_operation(anotherNumber, "-")

    def __mul__(self, anotherNumber):
        return self._internal_arithmetic_operation(anotherNumber, "*")

    def __truediv__(self, anotherNumber):
        return self._internal_arithmetic_operation(anotherNumber, "/")
    
    
    def __radd__(self, anotherNumber):
        return self + anotherNumber

    def __rsub__(self, anotherNumber):
        return numberWithUncertainty(anotherNumber) - self 

    def __rmul__(self, anotherNumber):
        return self * anotherNumber

    def __rtruediv__(self, anotherNumber):
        return numberWithUncertainty(anotherNumber) / self 


    def __iadd__(self, anotherNumber):
        result = self + anotherNumber
        self.became_copy_of(result)
        return result

    def __isub__(self, anotherNumber):
        result = self - anotherNumber
        self.became_copy_of(result)
        return result

    def __imul__(self, anotherNumber):
        result = self * anotherNumber
        self.became_copy_of(result)
        return result
    
    def  __itruediv__(self, anotherNumber):
        result = self / anotherNumber
        self.became_copy_of(result)
        return result
    
    
    def __pow__(self, exp):
        newVal = self.value**exp
        return numberWithUncertainty(newVal, (self.uncertainty / self.value) * exp * newVal)
    
    def sqrt(self):
        return self ** 0.5
    
    # Private Internal Comparasion ----
    def _internal_compare(self, anotherNumber, comparator):
        assert (comparator in self.INTERNAL_ALLOWED_COMPARASIONS), f"Comparator in this Function should be an internal allowed comparator: {self.INTERNAL_ALLOWED_COMPARASIONS}"
        
        anotherNumber = self._guarantee_number_w_uncertainty(anotherNumber)
        
        if comparator == "==":
            return (self.value == anotherNumber.value) and (self.uncertainty == anotherNumber.uncertainty)
        else:
            return eval(f"{self.value} {comparator} {anotherNumber.value}")
        
        
    # Comparasion Magic Methods ---    
    def __gt__(self, anotherNumber):
        return self._internal_compare(anotherNumber, ">")
    
    def __ge__(self, anotherNumber):
        return self._internal_compare(anotherNumber, ">=")
    
    def __lt__(self, anotherNumber):
        return self._internal_compare(anotherNumber, "<")
    
    def __le__(self, anotherNumber):
        return self._internal_compare(anotherNumber, "<=")

    def __eq__(self, anotherNumber):
        return self._internal_compare(anotherNumber, "==")
    
    def __ne__(self, anotherNumber):
        return (not self == anotherNumber)
        

    # Extra Math Magic Methods ----
    def __abs__(self):
        return numberWithUncertainty(abs(self.value), self.uncertainty)

    def __round__(self, decimal_places):
        return numberWithUncertainty(round(self.value, decimal_places), round(self.uncertainty, decimal_places))

    # String Methods ----
    # def format(self, value_measure_unit="", uncertainty_measure_unit="", certain_value_decimal_places_amount=3, imprecision_decimal_places_amount=3):
    def format_in_str(self, unit_of_measurement="", decimal_places_precision=3):
        if self.uncertainty == 0:
            return str(self.value)+unit_of_measurement
        else:
            final_str = ""
            
            if (type(self.value) is self.__class__):
                final_str = final_str + f"({round(self.value, decimal_places_precision)}{unit_of_measurement}) ± "
            else:
                final_str = final_str + f"{round(self.value, decimal_places_precision)}{unit_of_measurement} ± "
                
            if (type(self.uncertainty) is self.__class__):
                final_str = final_str + f"({round(self.uncertainty, decimal_places_precision)}{unit_of_measurement})"
            else:
                final_str = final_str + f"{round(self.uncertainty, decimal_places_precision)}{unit_of_measurement}"
                
            return final_str
                # return f"{round(self.value, decimal_places_precision)}{unit_of_measurement} ± {round(self.uncertainty, decimal_places_precision)}{unit_of_measurement}"

    def __str__(self):
        return self.format_in_str()
    
    
    # Number Conversion Magic Methods ----
    def __float__(self):
        return float(self.value)
    
    def __int__(self):
        return int(self.value)
    
    
    # Numpy Methods ---
    def conjugate(self):
        return numberWithUncertainty(self.value, self.uncertainty)
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.value}, {self.uncertainty})"
        
    

# FIXME Security Breach
# a = numberWithUncertainty(1, 1)
# a.value = "print('Security Breach!!')"
# a + 2