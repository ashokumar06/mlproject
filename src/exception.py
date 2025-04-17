import sys

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exe_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = f"Error occurred in script name [{filename}] line number [ {line_number} ] error message [{str(error)}]"
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detels:sys):
        self.error_message = error_message_detail(error_message,error_detels=error_detels)
        super().__init__(self.error_message)

    def __str__(self):
        
        return self.error_message    
