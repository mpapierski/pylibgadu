%module libgadu

%{
#include "/usr/local/include/libgadu.h"
%}

%typemap(in) va_list {
  // XXX: This is special workaround for function gg_vsaprint
}

%include "/usr/local/include/libgadu.h"
