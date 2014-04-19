# encoding: utf-8
# przykład prostego programu łączącego się z serwerem i wysyłającego
# jedną wiadomość.
import sys
import errno
import os
import libgadu


def main():
	#struct gg_session *sess;
	#struct gg_event *e;
	#struct gg_login_params p;

	if len(sys.argv) < 5:
		sys.stderr.write("użycie: {} <mójnumerek> <mojehasło> <numerek> <wiadomość>\n".format(sys.argv[0]))
		sys.exit(1)

	libgadu.gg_debug_level = 255;

	p = libgadu.gg_login_params()
	p.uin = int(sys.argv[1])
	p.password = sys.argv[2]
	try:
		sess = libgadu.gg_login(p)
	except IOError as e:
		sys.stderr.write("Nie udało się połączyć: {}\n".format(e.strerror))
		sys.exit(1)

	sys.stdout.write("Połączono.\n")

	# serwery gg nie pozwalaja wysylac wiadomosci bez powiadomienia o userliscie (przetestowane p.protocol_version [0x15; def])
	try:
		libgadu.gg_notify(sess, None, 0)
	except IOError as e:
		sys.stdout.write("Połączenie przerwane: {}\n".format(e.strerror))
		sys.exit(1)

	if libgadu.gg_send_message(sess, libgadu.GG_CLASS_MSG, int(sys.argv[3]), sys.argv[4]) == -1:
		sys.stdout.write("Połączenie przerwane: {}\n".format('errno'))
		libgadu.gg_free_session(sess)
		sys.exit(1)

	while True:
		e = libgadu.gg_watch_fd(sess)
		if e is None:
			sys.stdout.write("Połączenie przerwane: {}\n".format('errno'))
			libgadu.gg_logoff(sess)
			libgadu.gg_free_session(sess)
			sys.exit(1)

		if e.type == libgadu.GG_EVENT_ACK:
			sys.stdout.write("Wysłano.\n")
			libgadu.gg_free_event(e)
			break

		libgadu.gg_free_event(e)

	libgadu.gg_logoff(sess)
	libgadu.gg_free_session(sess)

if __name__ == '__main__':
	main()