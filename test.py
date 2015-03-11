__author__ = 'heru'
import json

import bpjs



if "__main__" == __name__:
    CUSTOMER_ID = "1000"
    SECRET_KEY = "1112"

    router = bpjs.BpjsBriding(CUSTOMER_ID, SECRET_KEY)
    # data = router.search_peserta_based_kartu("0000419274088")
    # print data
    # data = router.search_peserta_based_nik("3201152704890003")
    # info = json.loads(data)
    # print info['response']['list'][0]['nik']
    # print(router.search_rujukan_based_bpjs("0000017255248"))
    # print(
    #     router.search_daftar_pasien_based_date(limit=1)
    # )
    xml = """
        <?xml version='1.0' encoding='utf-8'?>
        <request>
         <data>
          <t_sep>
           <noKartu>0000017255248</noKartu>
           <tglSep>2015-03-11 11:35:03</tglSep>
           <tglRujukan>2015-03-05 13:05:03</tglRujukan>
           <noRujukan>1234590000300003</noRujukan>
           <ppkRujukan>09030204</ppkRujukan>
           <ppkPelayanan>0901R001</ppkPelayanan>
           <jnsPelayanan>1</jnsPelayanan>
           <catatan>dari WS</catatan>
           <diagAwal>N830</diagAwal>
           <poliTujuan>MAT</poliTujuan>
           <klsRawat>2</klsRawat>
           <user>JD</user>
           <noMr>1234</noMr>
          </t_sep>
         </data>
        </request>
    """
    print(
        router.sep(xml)
    )