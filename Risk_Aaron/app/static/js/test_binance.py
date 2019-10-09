import json

a = """[{"symbol":"ETHBTC","price":"0.02672000"},{"symbol":"LTCBTC","price":"0.01115100"},{"symbol":"BNBBTC","price":"0.00292100"},{"symbol":"NEOBTC","price":"0.00150700"},{"symbol":"QTUMETH","price":"0.01696500"},{"symbol":"EOSETH","price":"0.01988600"},{"symbol":"SNTETH","price":"0.00009480"},{"symbol":"BNTETH","price":"0.00247600"},{"symbol":"BCCBTC","price":"0.07908100"},{"symbol":"GASBTC","price":"0.00029500"},{"symbol":"BNBETH","price":"0.10928000"},{"symbol":"BTCUSDT","price":"11118.76000000"},{"symbol":"ETHUSDT","price":"297.08000000"},{"symbol":"HSRBTC","price":"0.00041400"},{"symbol":"OAXETH","price":"0.00062070"},{"symbol":"DNTETH","price":"0.00005707"},{"symbol":"MCOETH","price":"0.02085100"},{"symbol":"ICNETH","price":"0.00166300"},{"symbol":"MCOBTC","price":"0.00055900"},{"symbol":"WTCBTC","price":"0.00013110"},{"symbol":"WTCETH","price":"0.00490600"},{"symbol":"LRCBTC","price":"0.00000509"},{"symbol":"LRCETH","price":"0.00018918"},{"symbol":"QTUMBTC","price":"0.00045300"},{"symbol":"YOYOBTC","price":"0.00000274"},{"symbol":"OMGBTC","price":"0.00022800"},{"symbol":"OMGETH","price":"0.00848400"},{"symbol":"ZRXBTC","price":"0.00002753"},{"symbol":"ZRXETH","price":"0.00102934"},{"symbol":"STRATBTC","price":"0.00008110"},{"symbol":"STRATETH","price":"0.00303200"},{"symbol":"SNGLSBTC","price":"0.00000132"},{"symbol":"SNGLSETH","price":"0.00004902"},{"symbol":"BQXBTC","price":"0.00000897"},{"symbol":"BQXETH","price":"0.00033750"},{"symbol":"KNCBTC","price":"0.00002303"},{"symbol":"KNCETH","price":"0.00085960"},{"symbol":"FUNBTC","price":"0.00000046"},{"symbol":"FUNETH","price":"0.00001685"},{"symbol":"SNMBTC","price":"0.00000183"},{"symbol":"SNMETH","price":"0.00006831"},{"symbol":"NEOETH","price":"0.05631600"},{"symbol":"IOTABTC","price":"0.00003623"},{"symbol":"IOTAETH","price":"0.00135699"},{"symbol":"LINKBTC","price":"0.00031238"},{"symbol":"LINKETH","price":"0.01170915"},{"symbol":"XVGBTC","price":"0.00000074"},{"symbol":"XVGETH","price":"0.00002732"},{"symbol":"SALTBTC","price":"0.00004250"},{"symbol":"SALTETH","price":"0.00113800"},{"symbol":"MDABTC","price":"0.00007651"},{"symbol":"MDAETH","price":"0.00285800"},{"symbol":"MTLBTC","price":"0.00004880"},{"symbol":"MTLETH","price":"0.00182400"},{"symbol":"SUBBTC","price":"0.00000457"},{"symbol":"SUBETH","price":"0.00012334"},{"symbol":"EOSBTC","price":"0.00053120"},{"symbol":"SNTBTC","price":"0.00000254"},{"symbol":"ETCETH","price":"0.02687000"},{"symbol":"ETCBTC","price":"0.00071900"},{"symbol":"MTHBTC","price":"0.00000205"},{"symbol":"MTHETH","price":"0.00007655"},{"symbol":"ENGBTC","price":"0.00004931"},{"symbol":"ENGETH","price":"0.00184200"},{"symbol":"DNTBTC","price":"0.00000153"},{"symbol":"ZECBTC","price":"0.00945800"},{"symbol":"ZECETH","price":"0.35326000"},{"symbol":"BNTBTC","price":"0.00006653"},{"symbol":"ASTBTC","price":"0.00000525"},{"symbol":"ASTETH","price":"0.00019540"},{"symbol":"DASHBTC","price":"0.01422000"},{"symbol":"DASHETH","price":"0.53259000"},{"symbol":"OAXBTC","price":"0.00001657"},{"symbol":"ICNBTC","price":"0.00005742"},{"symbol":"BTGBTC","price":"0.00242200"},{"symbol":"BTGETH","price":"0.09099800"},{"symbol":"EVXBTC","price":"0.00006525"},{"symbol":"EVXETH","price":"0.00244770"},{"symbol":"REQBTC","price":"0.00000184"},{"symbol":"REQETH","price":"0.00006887"},{"symbol":"VIBBTC","price":"0.00000385"},{"symbol":"VIBETH","price":"0.00014338"},{"symbol":"HSRETH","price":"0.01247400"},{"symbol":"TRXBTC","price":"0.00000295"},{"symbol":"TRXETH","price":"0.00011069"},{"symbol":"POWRBTC","price":"0.00000993"},{"symbol":"POWRETH","price":"0.00037237"},{"symbol":"ARKBTC","price":"0.00004080"},{"symbol":"ARKETH","price":"0.00152400"},{"symbol":"YOYOETH","price":"0.00010280"},{"symbol":"XRPBTC","price":"0.00003697"},{"symbol":"XRPETH","price":"0.00138321"},{"symbol":"MODBTC","price":"0.00004280"},{"symbol":"MODETH","price":"0.00116700"},{"symbol":"ENJBTC","price":"0.00001155"},{"symbol":"ENJETH","price":"0.00043427"},{"symbol":"STORJBTC","price":"0.00002358"},{"symbol":"STORJETH","price":"0.00088760"},{"symbol":"BNBUSDT","price":"32.48230000"},{"symbol":"VENBNB","price":"0.14920000"},{"symbol":"YOYOBNB","price":"0.00093400"},{"symbol":"POWRBNB","price":"0.00338000"},{"symbol":"VENBTC","price":"0.00013928"},{"symbol":"VENETH","price":"0.00325194"},{"symbol":"KMDBTC","price":"0.00012540"},{"symbol":"KMDETH","price":"0.00467600"},{"symbol":"NULSBNB","price":"0.02662000"},{"symbol":"RCNBTC","price":"0.00000244"},{"symbol":"RCNETH","price":"0.00009045"},{"symbol":"RCNBNB","price":"0.00082800"},{"symbol":"NULSBTC","price":"0.00007788"},{"symbol":"NULSETH","price":"0.00292868"},{"symbol":"RDNBTC","price":"0.00003000"},{"symbol":"RDNETH","price":"0.00111800"},{"symbol":"RDNBNB","price":"0.01025000"},{"symbol":"XMRBTC","price":"0.00817800"},{"symbol":"XMRETH","price":"0.30608000"},{"symbol":"DLTBNB","price":"0.00300000"},{"symbol":"WTCBNB","price":"0.04480000"},{"symbol":"DLTBTC","price":"0.00000876"},{"symbol":"DLTETH","price":"0.00033026"},{"symbol":"AMBBTC","price":"0.00000356"},{"symbol":"AMBETH","price":"0.00013436"},{"symbol":"AMBBNB","price":"0.00122000"},{"symbol":"BCCETH","price":"2.47246000"},{"symbol":"BCCUSDT","price":"448.70000000"},{"symbol":"BCCBNB","price":"54.29000000"},{"symbol":"BATBTC","price":"0.00003007"},{"symbol":"BATETH","price":"0.00112645"},{"symbol":"BATBNB","price":"0.01030000"},{"symbol":"BCPTBTC","price":"0.00000508"},{"symbol":"BCPTETH","price":"0.00019000"},{"symbol":"BCPTBNB","price":"0.00174000"},{"symbol":"ARNBTC","price":"0.00003785"},{"symbol":"ARNETH","price":"0.00141659"},{"symbol":"GVTBTC","price":"0.00028140"},{"symbol":"GVTETH","price":"0.01051100"},{"symbol":"CDTBTC","price":"0.00000230"},{"symbol":"CDTETH","price":"0.00008635"},{"symbol":"GXSBTC","price":"0.00019120"},{"symbol":"GXSETH","price":"0.00714400"},{"symbol":"NEOUSDT","price":"16.75300000"},{"symbol":"NEOBNB","price":"0.51700000"},{"symbol":"POEBTC","price":"0.00000051"},{"symbol":"POEETH","price":"0.00001891"},{"symbol":"QSPBTC","price":"0.00000190"},{"symbol":"QSPETH","price":"0.00007140"},{"symbol":"QSPBNB","price":"0.00065000"},{"symbol":"BTSBTC","price":"0.00000572"},{"symbol":"BTSETH","price":"0.00021300"},{"symbol":"BTSBNB","price":"0.00196000"},{"symbol":"XZCBTC","price":"0.00106000"},{"symbol":"XZCETH","price":"0.03979200"},{"symbol":"XZCBNB","price":"0.36100000"},{"symbol":"LSKBTC","price":"0.00016490"},{"symbol":"LSKETH","price":"0.00618200"},{"symbol":"LSKBNB","price":"0.05610000"},{"symbol":"TNTBTC","price":"0.00000548"},{"symbol":"TNTETH","price":"0.00020485"},{"symbol":"FUELBTC","price":"0.00000066"},{"symbol":"FUELETH","price":"0.00002454"},{"symbol":"MANABTC","price":"0.00000450"},{"symbol":"MANAETH","price":"0.00016821"},{"symbol":"BCDBTC","price":"0.00010400"},{"symbol":"BCDETH","price":"0.00390000"},{"symbol":"DGDBTC","price":"0.00240600"},{"symbol":"DGDETH","price":"0.08955000"},{"symbol":"IOTABNB","price":"0.01238000"},{"symbol":"ADXBTC","price":"0.00001206"},{"symbol":"ADXETH","price":"0.00044960"},{"symbol":"ADXBNB","price":"0.00416000"},{"symbol":"ADABTC","price":"0.00000760"},{"symbol":"ADAETH","price":"0.00028462"},{"symbol":"PPTBTC","price":"0.00006040"},{"symbol":"PPTETH","price":"0.00225500"},{"symbol":"CMTBTC","price":"0.00000371"},{"symbol":"CMTETH","price":"0.00013825"},{"symbol":"CMTBNB","price":"0.00126000"},{"symbol":"XLMBTC","price":"0.00000977"},{"symbol":"XLMETH","price":"0.00036328"},{"symbol":"XLMBNB","price":"0.00333000"},{"symbol":"CNDBTC","price":"0.00000123"},{"symbol":"CNDETH","price":"0.00004591"},{"symbol":"CNDBNB","price":"0.00041900"},{"symbol":"LENDBTC","price":"0.00000068"},{"symbol":"LENDETH","price":"0.00002531"},{"symbol":"WABIBTC","price":"0.00002112"},{"symbol":"WABIETH","price":"0.00079000"},{"symbol":"WABIBNB","price":"0.00731000"},{"symbol":"LTCETH","price":"0.41766000"},{"symbol":"LTCUSDT","price":"123.91000000"},{"symbol":"LTCBNB","price":"3.81000000"},{"symbol":"TNBBTC","price":"0.00000061"},{"symbol":"TNBETH","price":"0.00002293"},{"symbol":"WAVESBTC","price":"0.00017210"},{"symbol":"WAVESETH","price":"0.00643000"},{"symbol":"WAVESBNB","price":"0.05890000"},{"symbol":"GTOBTC","price":"0.00000268"},{"symbol":"GTOETH","price":"0.00010054"},{"symbol":"GTOBNB","price":"0.00091000"},{"symbol":"ICXBTC","price":"0.00002850"},{"symbol":"ICXETH","price":"0.00106100"},{"symbol":"ICXBNB","price":"0.00975000"},{"symbol":"OSTBTC","price":"0.00000197"},{"symbol":"OSTETH","price":"0.00007353"},{"symbol":"OSTBNB","price":"0.00067300"},{"symbol":"ELFBTC","price":"0.00001835"},{"symbol":"ELFETH","price":"0.00068852"},{"symbol":"AIONBTC","price":"0.00001200"},{"symbol":"AIONETH","price":"0.00044500"},{"symbol":"AIONBNB","price":"0.00408000"},{"symbol":"NEBLBTC","price":"0.00010110"},{"symbol":"NEBLETH","price":"0.00374900"},{"symbol":"NEBLBNB","price":"0.03486000"},{"symbol":"BRDBTC","price":"0.00003224"},{"symbol":"BRDETH","price":"0.00119930"},{"symbol":"BRDBNB","price":"0.01100000"},{"symbol":"MCOBNB","price":"0.19039000"},{"symbol":"EDOBTC","price":"0.00008110"},{"symbol":"EDOETH","price":"0.00302400"},{"symbol":"WINGSBTC","price":"0.00001193"},{"symbol":"WINGSETH","price":"0.00033460"},{"symbol":"NAVBTC","price":"0.00001870"},{"symbol":"NAVETH","price":"0.00069800"},{"symbol":"NAVBNB","price":"0.00640000"},{"symbol":"LUNBTC","price":"0.00018500"},{"symbol":"LUNETH","price":"0.00695600"},{"symbol":"TRIGBTC","price":"0.00001980"},{"symbol":"TRIGETH","price":"0.00059400"},{"symbol":"TRIGBNB","price":"0.01218000"},{"symbol":"APPCBTC","price":"0.00000739"},{"symbol":"APPCETH","price":"0.00027710"},{"symbol":"APPCBNB","price":"0.00251000"},{"symbol":"VIBEBTC","price":"0.00000304"},{"symbol":"VIBEETH","price":"0.00011400"},{"symbol":"RLCBTC","price":"0.00003670"},{"symbol":"RLCETH","price":"0.00136500"},{"symbol":"RLCBNB","price":"0.01258000"},{"symbol":"INSBTC","price":"0.00002980"},{"symbol":"INSETH","price":"0.00111000"},{"symbol":"PIVXBTC","price":"0.00005670"},{"symbol":"PIVXETH","price":"0.00213200"},{"symbol":"PIVXBNB","price":"0.01945000"},{"symbol":"IOSTBTC","price":"0.00000113"},{"symbol":"IOSTETH","price":"0.00004232"},{"symbol":"CHATBTC","price":"0.00000195"},{"symbol":"CHATETH","price":"0.00006585"},{"symbol":"STEEMBTC","price":"0.00003260"},{"symbol":"STEEMETH","price":"0.00121800"},{"symbol":"STEEMBNB","price":"0.01118000"},{"symbol":"NANOBTC","price":"0.00011630"},{"symbol":"NANOETH","price":"0.00435100"},{"symbol":"NANOBNB","price":"0.03970000"},{"symbol":"VIABTC","price":"0.00003980"},{"symbol":"VIAETH","price":"0.00148600"},{"symbol":"VIABNB","price":"0.01350000"},{"symbol":"BLZBTC","price":"0.00000496"},{"symbol":"BLZETH","price":"0.00018634"},{"symbol":"BLZBNB","price":"0.00169000"},{"symbol":"AEBTC","price":"0.00004250"},{"symbol":"AEETH","price":"0.00158700"},{"symbol":"AEBNB","price":"0.01463000"},{"symbol":"RPXBTC","price":"0.00000224"},{"symbol":"RPXETH","price":"0.00005449"},{"symbol":"RPXBNB","price":"0.00145700"},{"symbol":"NCASHBTC","price":"0.00000026"},{"symbol":"NCASHETH","price":"0.00000969"},{"symbol":"NCASHBNB","price":"0.00008900"},{"symbol":"POABTC","price":"0.00000294"},{"symbol":"POAETH","price":"0.00010998"},{"symbol":"POABNB","price":"0.00100000"},{"symbol":"ZILBTC","price":"0.00000156"},{"symbol":"ZILETH","price":"0.00005829"},{"symbol":"ZILBNB","price":"0.00053300"},{"symbol":"ONTBTC","price":"0.00013190"},{"symbol":"ONTETH","price":"0.00493000"},{"symbol":"ONTBNB","price":"0.04506000"},{"symbol":"STORMBTC","price":"0.00000026"},{"symbol":"STORMETH","price":"0.00000949"},{"symbol":"STORMBNB","price":"0.00008700"},{"symbol":"QTUMBNB","price":"0.15510000"},{"symbol":"QTUMUSDT","price":"5.03400000"},{"symbol":"XEMBTC","price":"0.00000848"},{"symbol":"XEMETH","price":"0.00031637"},{"symbol":"XEMBNB","price":"0.00290000"},{"symbol":"WANBTC","price":"0.00003280"},{"symbol":"WANETH","price":"0.00123200"},{"symbol":"WANBNB","price":"0.01128000"},{"symbol":"WPRBTC","price":"0.00000102"},{"symbol":"WPRETH","price":"0.00003855"},{"symbol":"QLCBTC","price":"0.00000296"},{"symbol":"QLCETH","price":"0.00011135"},{"symbol":"SYSBTC","price":"0.00000409"},{"symbol":"SYSETH","price":"0.00015330"},{"symbol":"SYSBNB","price":"0.00139000"},{"symbol":"QLCBNB","price":"0.00101100"},{"symbol":"GRSBTC","price":"0.00003430"},{"symbol":"GRSETH","price":"0.00128043"},{"symbol":"ADAUSDT","price":"0.08457000"},{"symbol":"ADABNB","price":"0.00260000"},{"symbol":"CLOAKBTC","price":"0.00015550"},{"symbol":"CLOAKETH","price":"0.00414200"},{"symbol":"GNTBTC","price":"0.00000860"},{"symbol":"GNTETH","price":"0.00032155"},{"symbol":"GNTBNB","price":"0.00294000"},{"symbol":"LOOMBTC","price":"0.00000594"},{"symbol":"LOOMETH","price":"0.00022287"},{"symbol":"LOOMBNB","price":"0.00203000"},{"symbol":"XRPUSDT","price":"0.41108000"},{"symbol":"BCNBTC","price":"0.00000022"},{"symbol":"BCNETH","price":"0.00000707"},{"symbol":"BCNBNB","price":"0.00002000"},{"symbol":"REPBTC","price":"0.00144500"},{"symbol":"REPETH","price":"0.05421000"},{"symbol":"REPBNB","price":"0.49400000"},{"symbol":"BTCTUSD","price":"11057.22000000"},{"symbol":"TUSDBTC","price":"0.00025971"},{"symbol":"ETHTUSD","price":"295.79000000"},{"symbol":"TUSDETH","price":"0.00762097"},{"symbol":"TUSDBNB","price":"0.06777000"},{"symbol":"ZENBTC","price":"0.00086200"},{"symbol":"ZENETH","price":"0.03226000"},{"symbol":"ZENBNB","price":"0.29300000"},{"symbol":"SKYBTC","price":"0.00016800"},{"symbol":"SKYETH","price":"0.00628000"},{"symbol":"SKYBNB","price":"0.05800000"},{"symbol":"EOSUSDT","price":"5.90650000"},{"symbol":"EOSBNB","price":"0.18190000"},{"symbol":"CVCBTC","price":"0.00000656"},{"symbol":"CVCETH","price":"0.00024514"},{"symbol":"CVCBNB","price":"0.00220000"},{"symbol":"THETABTC","price":"0.00001094"},{"symbol":"THETAETH","price":"0.00040889"},{"symbol":"THETABNB","price":"0.00374000"},{"symbol":"XRPBNB","price":"0.01267000"},{"symbol":"TUSDUSDT","price":"1.00610000"},{"symbol":"IOTAUSDT","price":"0.40280000"},{"symbol":"XLMUSDT","price":"0.10860000"},{"symbol":"IOTXBTC","price":"0.00000076"},{"symbol":"IOTXETH","price":"0.00002817"},{"symbol":"QKCBTC","price":"0.00000197"},{"symbol":"QKCETH","price":"0.00007400"},{"symbol":"AGIBTC","price":"0.00000334"},{"symbol":"AGIETH","price":"0.00012467"},{"symbol":"AGIBNB","price":"0.00114000"},{"symbol":"NXSBTC","price":"0.00002860"},{"symbol":"NXSETH","price":"0.00105500"},{"symbol":"NXSBNB","price":"0.00970000"},{"symbol":"ENJBNB","price":"0.00397500"},{"symbol":"DATABTC","price":"0.00000187"},{"symbol":"DATAETH","price":"0.00006984"},{"symbol":"ONTUSDT","price":"1.46700000"},{"symbol":"TRXBNB","price":"0.00101300"},{"symbol":"TRXUSDT","price":"0.03286000"},{"symbol":"ETCUSDT","price":"7.98880000"},{"symbol":"ETCBNB","price":"0.24510000"},{"symbol":"ICXUSDT","price":"0.31610000"},{"symbol":"SCBTC","price":"0.00000030"},{"symbol":"SCETH","price":"0.00001084"},{"symbol":"SCBNB","price":"0.00010000"},{"symbol":"NPXSBTC","price":"0.00000009"},{"symbol":"NPXSETH","price":"0.00000303"},{"symbol":"VENUSDT","price":"0.00010000"},{"symbol":"KEYBTC","price":"0.00000027"},{"symbol":"KEYETH","price":"0.00001014"},{"symbol":"NASBTC","price":"0.00013400"},{"symbol":"NASETH","price":"0.00502800"},{"symbol":"NASBNB","price":"0.04591000"},{"symbol":"MFTBTC","price":"0.00000024"},{"symbol":"MFTETH","price":"0.00000893"},{"symbol":"MFTBNB","price":"0.00008200"},{"symbol":"DENTBTC","price":"0.00000014"},{"symbol":"DENTETH","price":"0.00000522"},{"symbol":"ARDRBTC","price":"0.00001010"},{"symbol":"ARDRETH","price":"0.00037814"},{"symbol":"ARDRBNB","price":"0.00344000"},{"symbol":"NULSUSDT","price":"0.86510000"},{"symbol":"HOTBTC","price":"0.00000018"},{"symbol":"HOTETH","price":"0.00000684"},{"symbol":"VETBTC","price":"0.00000075"},{"symbol":"VETETH","price":"0.00002830"},{"symbol":"VETUSDT","price":"0.00839900"},{"symbol":"VETBNB","price":"0.00025940"},{"symbol":"DOCKBTC","price":"0.00000119"},{"symbol":"DOCKETH","price":"0.00004391"},{"symbol":"POLYBTC","price":"0.00000766"},{"symbol":"POLYBNB","price":"0.00262000"},{"symbol":"PHXBTC","price":"0.00000180"},{"symbol":"PHXETH","price":"0.00005617"},{"symbol":"PHXBNB","price":"0.00045600"},{"symbol":"HCBTC","price":"0.00042740"},{"symbol":"HCETH","price":"0.01597000"},{"symbol":"GOBTC","price":"0.00000167"},{"symbol":"GOBNB","price":"0.00057100"},{"symbol":"PAXBTC","price":"0.00025175"},{"symbol":"PAXBNB","price":"0.20121000"},{"symbol":"PAXUSDT","price":"1.00610000"},{"symbol":"PAXETH","price":"0.00888047"},{"symbol":"RVNBTC","price":"0.00000501"},{"symbol":"RVNBNB","price":"0.00172200"},{"symbol":"DCRBTC","price":"0.00283100"},{"symbol":"DCRBNB","price":"0.96400000"},{"symbol":"USDCBNB","price":"0.21755000"},{"symbol":"USDCBTC","price":"0.00031132"},{"symbol":"MITHBTC","price":"0.00000372"},{"symbol":"MITHBNB","price":"0.00127000"},{"symbol":"BCHABCBTC","price":"0.03716700"},{"symbol":"BCHSVBTC","price":"0.01117900"},{"symbol":"BCHABCUSDT","price":"413.11000000"},{"symbol":"BCHSVUSDT","price":"58.90000000"},{"symbol":"BNBPAX","price":"32.38900000"},{"symbol":"BTCPAX","price":"11048.72000000"},{"symbol":"ETHPAX","price":"295.05000000"},{"symbol":"XRPPAX","price":"0.40827000"},{"symbol":"EOSPAX","price":"5.86500000"},{"symbol":"XLMPAX","price":"0.10798000"},{"symbol":"RENBTC","price":"0.00000692"},{"symbol":"RENBNB","price":"0.00237000"},{"symbol":"BNBTUSD","price":"32.24000000"},{"symbol":"XRPTUSD","price":"0.40815000"},{"symbol":"EOSTUSD","price":"5.84860000"},{"symbol":"XLMTUSD","price":"0.10828000"},{"symbol":"BNBUSDC","price":"32.26110000"},{"symbol":"BTCUSDC","price":"11045.58000000"},{"symbol":"ETHUSDC","price":"295.44000000"},{"symbol":"XRPUSDC","price":"0.40932000"},{"symbol":"EOSUSDC","price":"5.82870000"},{"symbol":"XLMUSDC","price":"0.10779000"},{"symbol":"USDCUSDT","price":"1.00640000"},{"symbol":"ADATUSD","price":"0.08422000"},{"symbol":"TRXTUSD","price":"0.03259000"},{"symbol":"NEOTUSD","price":"16.65100000"},{"symbol":"TRXXRP","price":"0.08002000"},{"symbol":"XZCXRP","price":"28.82500000"},{"symbol":"PAXTUSD","price":"1.00040000"},{"symbol":"USDCTUSD","price":"0.99970000"},{"symbol":"USDCPAX","price":"0.99990000"},{"symbol":"LINKUSDT","price":"3.47480000"},{"symbol":"LINKTUSD","price":"3.47440000"},{"symbol":"LINKPAX","price":"3.44160000"},{"symbol":"LINKUSDC","price":"3.44890000"},{"symbol":"WAVESUSDT","price":"1.91720000"},{"symbol":"WAVESTUSD","price":"1.88950000"},{"symbol":"WAVESPAX","price":"1.91760000"},{"symbol":"WAVESUSDC","price":"1.88720000"},{"symbol":"BCHABCTUSD","price":"410.80000000"},{"symbol":"BCHABCPAX","price":"410.49000000"},{"symbol":"BCHABCUSDC","price":"410.93000000"},{"symbol":"BCHSVTUSD","price":"59.17000000"},{"symbol":"BCHSVPAX","price":"58.18000000"},{"symbol":"BCHSVUSDC","price":"57.50000000"},{"symbol":"LTCTUSD","price":"123.22000000"},{"symbol":"LTCPAX","price":"122.83000000"},{"symbol":"LTCUSDC","price":"122.90000000"},{"symbol":"TRXPAX","price":"0.03262000"},{"symbol":"TRXUSDC","price":"0.03260000"},{"symbol":"BTTBTC","price":"0.00000014"},{"symbol":"BTTBNB","price":"0.00004601"},{"symbol":"BTTUSDT","price":"0.00149590"},{"symbol":"BNBUSDS","price":"32.23000000"},{"symbol":"BTCUSDS","price":"11070.18000000"},{"symbol":"USDSUSDT","price":"1.00340000"},{"symbol":"USDSPAX","price":"0.99970000"},{"symbol":"USDSTUSD","price":"0.99880000"},{"symbol":"USDSUSDC","price":"0.99630000"},{"symbol":"BTTPAX","price":"0.00148000"},{"symbol":"BTTTUSD","price":"0.00148730"},{"symbol":"BTTUSDC","price":"0.00148410"},{"symbol":"ONGBNB","price":"0.01203000"},{"symbol":"ONGBTC","price":"0.00003493"},{"symbol":"ONGUSDT","price":"0.38870000"},{"symbol":"HOTBNB","price":"0.00006245"},{"symbol":"HOTUSDT","price":"0.00203550"},{"symbol":"ZILUSDT","price":"0.01730000"},{"symbol":"ZRXBNB","price":"0.00941000"},{"symbol":"ZRXUSDT","price":"0.30540000"},{"symbol":"FETBNB","price":"0.00488000"},{"symbol":"FETBTC","price":"0.00001432"},{"symbol":"FETUSDT","price":"0.15900000"},{"symbol":"BATUSDT","price":"0.33440000"},{"symbol":"XMRBNB","price":"2.80100000"},{"symbol":"XMRUSDT","price":"90.93000000"},{"symbol":"ZECBNB","price":"3.23500000"},{"symbol":"ZECUSDT","price":"105.26000000"},{"symbol":"ZECPAX","price":"104.49000000"},{"symbol":"ZECTUSD","price":"104.13000000"},{"symbol":"ZECUSDC","price":"104.93000000"},{"symbol":"IOSTBNB","price":"0.00038760"},{"symbol":"IOSTUSDT","price":"0.01258100"},{"symbol":"CELRBNB","price":"0.00053700"},{"symbol":"CELRBTC","price":"0.00000157"},{"symbol":"CELRUSDT","price":"0.01745000"},{"symbol":"ADAPAX","price":"0.08438000"},{"symbol":"ADAUSDC","price":"0.08438000"},{"symbol":"NEOPAX","price":"16.64200000"},{"symbol":"NEOUSDC","price":"16.72600000"},{"symbol":"DASHBNB","price":"4.86600000"},{"symbol":"DASHUSDT","price":"158.20000000"},{"symbol":"NANOUSDT","price":"1.29370000"},{"symbol":"OMGBNB","price":"0.07751000"},{"symbol":"OMGUSDT","price":"2.54480000"},{"symbol":"THETAUSDT","price":"0.12069000"},{"symbol":"ENJUSDT","price":"0.12861000"},{"symbol":"MITHUSDT","price":"0.04134000"},{"symbol":"MATICBNB","price":"0.00068800"},{"symbol":"MATICBTC","price":"0.00000202"},{"symbol":"MATICUSDT","price":"0.02238000"},{"symbol":"ATOMBNB","price":"0.17270000"},{"symbol":"ATOMBTC","price":"0.00050330"},{"symbol":"ATOMUSDT","price":"5.60400000"},{"symbol":"ATOMUSDC","price":"5.57800000"},{"symbol":"ATOMPAX","price":"5.65300000"},{"symbol":"ATOMTUSD","price":"5.57000000"},{"symbol":"ETCUSDC","price":"7.78600000"},{"symbol":"ETCPAX","price":"7.87300000"},{"symbol":"ETCTUSD","price":"7.88300000"},{"symbol":"BATUSDC","price":"0.33290000"},{"symbol":"BATPAX","price":"0.33300000"},{"symbol":"BATTUSD","price":"0.33310000"},{"symbol":"PHBBNB","price":"0.00043500"},{"symbol":"PHBBTC","price":"0.00000127"},{"symbol":"PHBUSDC","price":"0.01300000"},{"symbol":"PHBTUSD","price":"0.01378000"},{"symbol":"PHBPAX","price":"0.01372000"},{"symbol":"TFUELBNB","price":"0.00030100"},{"symbol":"TFUELBTC","price":"0.00000088"},{"symbol":"TFUELUSDT","price":"0.00977000"},{"symbol":"TFUELUSDC","price":"0.00993000"},{"symbol":"TFUELTUSD","price":"0.00970000"},{"symbol":"TFUELPAX","price":"0.00988000"},{"symbol":"ONEBNB","price":"0.00061200"},{"symbol":"ONEBTC","price":"0.00000179"},{"symbol":"ONEUSDT","price":"0.01981000"},{"symbol":"ONETUSD","price":"0.01949000"},{"symbol":"ONEPAX","price":"0.01962000"},{"symbol":"ONEUSDC","price":"0.01966000"},{"symbol":"FTMBNB","price":"0.00084900"},{"symbol":"FTMBTC","price":"0.00000248"},{"symbol":"FTMUSDT","price":"0.02750000"},{"symbol":"FTMTUSD","price":"0.02734000"},{"symbol":"FTMPAX","price":"0.02672000"},{"symbol":"FTMUSDC","price":"0.02712000"},{"symbol":"BTCBBTC","price":"0.99980000"},{"symbol":"BCPTTUSD","price":"0.05376000"},{"symbol":"BCPTPAX","price":"0.05267000"},{"symbol":"BCPTUSDC","price":"0.05181000"},{"symbol":"ALGOBNB","price":"0.04339000"},{"symbol":"ALGOBTC","price":"0.00012680"},{"symbol":"ALGOUSDT","price":"1.41300000"},{"symbol":"ALGOTUSD","price":"1.40600000"},{"symbol":"ALGOPAX","price":"1.42900000"},{"symbol":"ALGOUSDC","price":"1.40800000"},{"symbol":"USDSBUSDT","price":"1.00300000"},{"symbol":"USDSBUSDS","price":"0.99990000"}]"""

All = json.loads(a)

for all in All:
    if (all["symbol"].find("USD") >= 0 and all["symbol"].find("BTG") >= 0):
        print(all)

