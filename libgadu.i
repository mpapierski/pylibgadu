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

// Special case for sending message: Convert unsigned char * to char *.
%rename(gg_send_message) wrap_gg_send_message;
%inline %{
int wrap_gg_send_message(struct gg_session *sess, int msgclass, unsigned int recipient, const char *message)
{
	return gg_send_message(sess, msgclass, recipient, (const unsigned char *)message);
}
%}

// Raise exception from wrapped gg_send_message function
%exception gg_send_message {
	$action
	if (result == -1) {
		gg_free_session(arg1);
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
}

// Raise exception from wrapped gg_watch_fd function
%exception gg_watch_fd {
	$action
	if (result == -1) {
		gg_free_session(arg1);
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
}

%include "libgadu.h"

