import os
import idc
import idautils
import idaapi
import pickle
import ida_idaapi
import idaapi
import ida_nalt
import pathlib

idc.auto_wait()

input_path = pathlib.Path(ida_nalt.get_input_file_path())

save_path = input_path.parent / (input_path.stem + '.export')

idaapi.ida_expr.eval_idc_expr(None, ida_idaapi.BADADDR,
                              f'BinExportBinary("{save_path}");')

idc.qexit(0)
