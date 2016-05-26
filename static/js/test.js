{
    "cache": {
        "name": "Disk",
        "path": "/tmp/stache",
        "dirs": "portable",
	"verbose": "true"
    },
    "layers": {
        "bx_pluto_wm": {
            "allowed origin": "*",
            "provider": {
                "class": "TileStache.Goodies.VecTiles:Provider",
                "kwargs": {
		    "clip": "true",
		    "srid": "4326",	
                    "dbinfo": {
                        "host": "localhost",
			"user": "mario",
                        "database": "gis"
                    },
                    "queries": [                    
                        "SELECT geom as __geometry__, gid AS __id__ FROM bx_pluto_wm"
                    ]
        }}}
    }
}