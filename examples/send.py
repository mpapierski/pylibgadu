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

	sess = libgadu.gg_login(p)
	sys.stdout.write("Połączono.\n")
	
	# serwery gg nie pozwalaja wysylac wiadomosci bez powiadomienia o userliscie (przetestowane p.protocol_version [0x15; def])
	libgadu.gg_notify(sess, None, 0)
	delivery_code = libgadu.gg_send_message(sess, libgadu.GG_CLASS_MSG, int(sys.argv[3]), sys.argv[4])
	sys.stdout.write('delivery_code={}\n'.format(delivery_code))

	while True:
		try:
			e = libgadu.gg_watch_fd(sess)
			if e.type == libgadu.GG_EVENT_ACK:
				sys.stdout.write("Wysłano.\n")
				break
		except IOError as e:
			libgadu.gg_logoff(sess)
			libgadu.gg_free_session(sess)
			raise
		finally:
			libgadu.gg_free_event(e)

	libgadu.gg_logoff(sess)
	libgadu.gg_free_session(sess)

if __name__ == '__main__':
	try:
		main()
	except IOError as e:
		sys.stdout.write("Połączenie przerwane: {}\n".format(e.strerror))
		raise