#!/usr/bin/env python3

from sys import stdout
import os
import argparse
from typing import (Union, Optional, IO,
                   Callable, Hashable, Dict,
                   Any, Sequence)

import pandas as pd


def main(
         # input args
         read_path_or_buf: Union[str,os.PathLike,IO,pd.HDFStore], key: Union[str,object], 
         read_mode: str='r', errors: str='strict',
         where: Optional[Union[str,list[str]]]=None, start: Optional[int]=None,
         stop: Optional[int]=None, read_columns: Optional[list[str]]=None,
         iterator: Optional[bool]=False, chunksize: Optional[int]=None,
         pandas_print: Optional[bool]=True,
         # output args
         #write_path_or_buf: Optional[Union[str,IO,os.PathLike,None]]=None,
         #sep: Optional[str]=',', na_rep: Optional[str]='',
         #float_format: Optional[Union[str,Callable]]=None,
         #out_columns: Optional[Sequence[Hashable]]=None,
         #header: Optional[Union[bool,list[str]]]=True, index: Optional[bool]=True,
         #index_label: Optional[Union[Hashable,Sequence[Hashable]]]=None,
         # not written in comments yet
         #write_mode: Optional[]='w',
         #encoding: Optional[]=None, compression: Optional[]='infer',
         #quoting: Optional[]=None, quotechar: Optional[]='"',
         #lineterminator: Optional[]=None, chunksize: Optional[]=None,
         #date_format: Optional[]=None,
         #doublequote: Optional[]=True, escapechar: Optional[]=None,
         #decimal: Optional[]='.', errors: Optional[]='strict',
         #storage_options: Optional[Dict[str, Any]]=None
         **kwargs) -> object:
    r"""
    Print HDF5 files to terminal. Based on Pandas read_hdf.
    
    Read from the store, close it if we opened it.
    Retrieve pandas object stored in file, optionally based on where
    criteria.
    .. warning::
       Pandas uses PyTables for reading and writing HDF5 files, which allows
       serializing object-dtype data with pickle when using the "fixed" format.
       Loading pickled data received from untrusted sources can be unsafe.
       See: https://docs.python.org/3/library/pickle.html for more.
    
    Parameters
    ----------
    read_path_or_buf : str, path object, pandas.HDFStore
        Any valid string path is acceptable. Only supports the local file system,
        remote URLs and file-like objects are not supported.
        If you want to pass in a path object, pandas accepts any
        ``os.PathLike``.
        Alternatively, pandas accepts an open :class:`pandas.HDFStore` object.
    key : object, optional
        The group identifier in the store. Can be omitted if the HDF file
        contains a single pandas object.
    read_mode : {'r', 'r+', 'a'}, default 'r'
        Mode to use when opening the file. Ignored if read_path_or_buf is a
        :class:`pandas.HDFStore`. Default is 'r'.
    errors : str, default 'strict'
        Specifies how encoding and decoding errors are to be handled.
        See the errors argument for :func:`open` for a full list
        of options.
    where : list, optional
        A list of Term (or convertible) objects.
    start : int, optional
        Row number to start selection.
    stop  : int, optional
        Row number to stop selection.
    read_columns : list, optional
        A list of columns names to return.
    iterator : bool, optional
        Return an iterator object.
    chunksize : int, optional
        Number of rows to include in an iteration when using an iterator.
    **kwargs
        Additional keyword arguments passed to HDFStore.
    
    Returns
    -------
    item : object
        The selected object. Return type depends on the object stored.
    """
        
    # read
    hdf5_df = pd.read_hdf( read_path_or_buf, key, read_mode,
                           errors, where, start, stop, read_columns,
                           iterator, chunksize, **kwargs )
    
    # printing: print as panda or print as delimited file
    if pandas_print:
        with pd.option_context( 'expand_frame_repr', False,
                                'display.max_rows', None,
                                'display.precision', 4,
                                'display.max_colwidth', 15): 
            print(hdf5_df,file=stdout)
    else:
        NotImplementedError('ASCII file print not supported yet.')
        """
        hdf5_df.to_csv( write_path_or_buf=stdout,
                         sep, na_rep, float_format,
                        out_columns, header, index, index_label )
        """

    return hdf5_df

if __name__ == '__main__':
    
    # don't use typer. It doesn't accept union types
    #typer.run(main)

    parser = argparse.ArgumentParser(description='Output HDF5 table to stdout as ASCII text file.')
    
    read_group = parser.add_argument_group('Reading File','Arguments used to read file with pandas.read_hdf')
    read_group.add_argument('-r','--read-path-or-buf', help='File path to HDF5 file', type=str, required=True)
    read_group.add_argument('-k','--key', help='Key name to use within HDF5 file', type=str, required=True)
    read_group.add_argument('--start', help='Start index within HDF5 table', type=int, required=False)
    read_group.add_argument('--stop', help='Stop index within HDF5 table', type=int, required=False)
    read_group.add_argument('--read-columns', help='Columns to read within HDF5 table', type=list, nargs='+', required=False)
    
    #write_group = parser.add_argument_group('Writing File','Arguments used to write file with pandas.to_csv')
    #read_group.add_argument('-w','--write-path-or-buf', help='File path to write ASCII file to', type=str, required=False)
    #write_group.add_argument('-s','--sep', help='Separator to use', type=str, required=False)

    main(**vars(parser.parse_args()))
    
    """
    FOR WRITING:

    write_path_or_buf : str, path object, file-like object, or None, default None
        String, path object (implementing os.PathLike[str]), or file-like
        object implementing a write() function. If None, the result is
        returned as a string. If a non-binary file object is passed, it should
        be opened with `newline=''`, disabling universal newlines. If a binary
        file object is passed, `write_mode` might need to contain a `'b'`.
        .. versionchanged:: 1.2.0
           Support for binary file objects was introduced.
    sep : str, default ','
        String of length 1. Field delimiter for the output file.
    na_rep : str, default ''
        Missing data representation.
    float_format : str, Callable, default None
        Format string for floating point numbers. If a Callable is given, it takes
        precedence over other numeric formatting parameters, like decimal.
    out_columns : sequence, optional
        Columns to write.
    header : bool or list of str, default True
        Write out the column names. If a list of strings is given it is
        assumed to be aliases for the column names.
    index : bool, default True
        Write row names (index).
    index_label : str or sequence, or False, default None
        Column label for index column(s) if desired. If None is given, and
        `header` and `index` are True, then the index names are used. A
        sequence should be given if the object uses MultiIndex. If
        False do not print fields for index names. Use index_label=False
        for easier importing in R.
    write_mode : str, default 'w'
        Python write mode. The available write modes are the same as
        :py:func:`open`.
    encoding : str, optional
        A string representing the encoding to use in the output file,
        defaults to 'utf-8'. `encoding` is not supported if `write_path_or_buf`
        is a non-binary file object.
    quoting : optional constant from csv module
        Defaults to csv.QUOTE_MINIMAL. If you have set a `float_format`
        then floats are converted to strings and thus csv.QUOTE_NONNUMERIC
        will treat them as non-numeric.
    quotechar : str, default '\"'
        String of length 1. Character used to quote fields.
    lineterminator : str, optional
        The newline character or character sequence to use in the output
        file. Defaults to `os.linesep`, which depends on the OS in which
        this method is called ('\\n' for linux, '\\r\\n' for Windows, i.e.).
        .. versionchanged:: 1.5.0
            Previously was line_terminator, changed for consistency with
            read_csv and the standard library 'csv' module.
    chunksize : int or None
        Rows to write at a time.
    date_format : str, default None
        Format string for datetime objects.
    doublequote : bool, default True
        Control quoting of `quotechar` inside a field.
    escapechar : str, default None
        String of length 1. Character used to escape `sep` and `quotechar`
        when appropriate.
    decimal : str, default '.'
        Character recognized as decimal separator. E.g. use ',' for
        European data.
    errors : str, default 'strict'
        Specifies how encoding and decoding errors are to be handled.
        See the errors argument for :func:`open` for a full list
        of options.
    """


    """
    From numpy
        def to_csv(
        self,
        path_or_buf: FilePath | WriteBuffer[bytes] | WriteBuffer[str] | None = None,
        sep: str = ",",
        na_rep: str = "",
        float_format: str | Callable | None = None,
        columns: Sequence[Hashable] | None = None,
        header: bool_t | list[str] = True,
        index: bool_t = True,
        index_label: IndexLabel | None = None,
        mode: str = "w",
        encoding: str | None = None,
        compression: CompressionOptions = "infer",
        quoting: int | None = None,
        quotechar: str = '"',
        lineterminator: str | None = None,
        chunksize: int | None = None,
        date_format: str | None = None,
        doublequote: bool_t = True,
        escapechar: str | None = None,
        decimal: str = ".",
        errors: str = "strict",
        storage_options: StorageOptions = None,
    ) -> str | None:

    def read_hdf(
        path_or_buf: FilePath | HDFStore,
    key=None,
    mode: str = "r",
    errors: str = "strict",
    where: str | list | None = None,
    start: int | None = None,
    stop: int | None = None,
    columns: list[str] | None = None,
    iterator: bool = False,
    chunksize: int | None = None,
    **kwargs )
    """
