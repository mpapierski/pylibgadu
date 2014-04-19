%module libgadu

%{
#include "libgadu.h"
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

// gg_event_free is really gg_free_event
%rename(gg_free_event) gg_event_free(struct gg_event *);

// Raise exception from gg_login function
%exception gg_login {
	$action
	if (!result) {
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
}

// Raise exception from gg_login function
%exception gg_notify {
	$action
	if (result == -1) {
		gg_free_session(arg1);
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
}


%include "libgadu.h"

