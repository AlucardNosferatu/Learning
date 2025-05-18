from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

src_pl = "foo(a).\nfoo(b).\nfoo(c)."
# pengine_builder = PengineBuilder(urlserver="http://localhost:4242", srctext=src_pl)'
pengine_builder = PengineBuilder(urlserver="http://localhost:4242")
pengine = Pengine(builder=pengine_builder)
query = "member(X, [1,2,3])"
# query = "foo(X)"
pengine.doAsk(pengine.ask(query))
print(pengine.currentQuery.availProofs)
while pengine.currentQuery.hasMore:
    pengine.doNext(pengine.currentQuery)
    print(pengine.currentQuery.availProofs)
