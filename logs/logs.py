
import datetime
import os
import sys
##############################################################################################
####                                                                                      ####
####                                  For Error logging                                   ####
####                                                                                      ####
##############################################################################################



def createLogFile(log_folder_path):
    flog_fname = datetime.datetime.now().strftime('%b_%Y.txt')
    # if file does not exists
    if(not os.path.exists(os.path.join(log_folder_path, flog_fname))):
        # if log folder doesn't exist
        if (not os.path.exists(log_folder_path)):
            os.makedirs(log_folder_path)
        # if folder exists but file doesn't exists
        # temporary log file variable to create file
        try:
            flog = open(os.path.join(
                log_folder_path, flog_fname), 'w')
            flog.close()
        except FileNotFoundError:
            print(f"File {flog_fname} not found.  Aborting")
            sys.exit(1)
        except OSError:
            print(f"OS error occurred while trying to open file: {flog_fname}")
            sys.exit(1)
        except Exception as err:
            print(
                f"Unexpected {repr(err)} occured while opening file: {flog_fname}")
            raise
    # if file already exists
    # log file variable in append mode
    try:
        flog = open(os.path.join(
            log_folder_path, flog_fname), 'a')
    except OSError:
        print(f"OS error occurred while trying to open file: {flog_fname}")
        sys.exit(1)
    except Exception as err:
        print(
            f"Unexpected {repr(err)} occured while opening file: {flog_fname}")
        raise
    return flog

