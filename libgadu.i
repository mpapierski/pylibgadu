%module libgadu

%{
#include "/usr/local/include/libgadu.h"
%}

%typemap(in) va_list {
  // XXX: This is special workaround for function gg_vsaprint
}

// Handle uin_t as Python long type
%typemap(in) uin_t {
  $1 = PyInt_AsLong($input);
}

%typemap(out) uin_t {
  $result = PyInt_FromLong($1);
}

%include "/usr/local/include/libgadu.h"
