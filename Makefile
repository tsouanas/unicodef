default:
	cd src \
		&& sh mkunicodef.sh \
		&& mv defs.seq defs.exp unicodef.md XCompose-unicodef unicodef.vim ../build

install:
	mkdir -p ~/.unicodef \
		&& cp -p build/XCompose-unicodef build/unicodef.vim ~/.unicodef/

clean:
	rm -f build/defs.seq build/defs.exp

cleanall: clean
	rm -f build/unicodef.md build/XCompose-unicodef build/unicodef.vim
