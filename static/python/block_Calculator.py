from osgeo import ogr
import os
import time

start = time.time()

# identify input shapefile
source = ogr.Open('/Users/Mario/Documents/mario_nyc/postgres_nyc/shp/allCity2409vfin.shp', 1)

# dictionaries define the proportion of each use type for each building type, for use in calculating area by use later
propRes = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:1, 17:1, 18:1, 19:0.9612, 20:0.0076, 21:0.0039, 22:0.5574665, 23:0.0020886, 24:0.0223, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0.5086451, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}
propOff = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0.0071, 20:0.0257, 21:0.9405, 22:0.0035155, 23:0.4691626, 24:0.0122, 25:0, 26:0, 27:0, 28:0, 29:0.3147, 30:1, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0.4524893, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}
propRet = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0.0116, 20:0.9204, 21:0.0457, 22:0.4228065, 23:0.4092926, 24:0.0035, 25:0, 26:0, 27:0, 28:0, 29:0.1002, 30:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0.0171143, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}
propPa = {1:0, 2:0, 3:0.5, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:0, 26:1, 27:0, 28:1, 29:0, 30:0, 32:0, 33:0, 34:1, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:1, 59:1, 60:1, 61:1, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}
propGar = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0.02, 20:0.0463, 21:0.0088, 22:0.0162115, 23:0.1172256, 24:0.0087, 25:0, 26:0, 27:0, 28:0, 29:0.5851, 30:0, 32:0, 33:1, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0.0217513, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}
propFac = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0.0022306, 24:0, 25:1, 26:0, 27:1, 28:0, 29:0, 30:0, 32:1, 33:0, 34:0, 35:0, 36:0, 37:1, 38:1, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:1, 64:1, 65:1, 66:1, 67:1, 68:1, 69:1, 70:1, 71:1, 72:1, 73:0, 74:1, 75:0, 76:0, 77:0, 78:0, 79:0, 80:1, 81:0, 82:0}
propTrans = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:1, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:1, 40:1, 41:1, 43:1, 44:1, 45:1, 46:1, 47:1, 48:1, 49:1, 50:1, 51:0, 52:1, 53:0, 54:1, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:1, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:1, 76:0, 77:1, 78:1, 79:0, 80:0, 81:0, 82:0}
propHot = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0.0001, 20:0, 21:0, 22:0, 23:0, 24:0.9533, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0, 51:0, 52:0, 53:0, 54:0, 55:0, 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0, 72:0, 73:0, 74:0, 75:0, 76:0, 77:0, 78:0, 79:0, 80:0, 81:0, 82:0}

layer = source.GetLayer()
layer_defn = layer.GetLayerDefn()
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
print len(field_names) #checks to see whether we can access the fields in the shapefile

# # creates the necessary fields to store area calculated for each use
# print "Creating additional fields..."
# area_field = ogr.FieldDefn('bdg_area', ogr.OFTReal)
# layer.CreateField(area_field)
#
# res_field = ogr.FieldDefn('res_area', ogr.OFTReal)
# layer.CreateField(res_field)
#
# off_field = ogr.FieldDefn('off_area', ogr.OFTReal)
# layer.CreateField(off_field)
#
# ret_field = ogr.FieldDefn('ret_area', ogr.OFTReal)
# layer.CreateField(ret_field)
#
# pa_field = ogr.FieldDefn('pa_area', ogr.OFTReal)
# layer.CreateField(pa_field)
#
# gar_field = ogr.FieldDefn('gar_area', ogr.OFTReal)
# layer.CreateField(gar_field)
#
# fac_field = ogr.FieldDefn('fac_area', ogr.OFTReal)
# layer.CreateField(fac_field)
#
# trans_field = ogr.FieldDefn('trans_area', ogr.OFTReal)
# layer.CreateField(trans_field)
#
# hot_field = ogr.FieldDefn('hot_area', ogr.OFTReal)
# layer.CreateField(hot_field)
# print "Fields created."
#
# # next, need to multiply shape area by number of floors to get total building area
# print "Calculating total building area..."
# for row in layer:
#     geom = row.GetGeometryRef()
#     shapeArea = geom.GetArea()
#     numFloors = float(row.GetField('nmbrfloors'))
#     layer.SetFeature(row)
#     row.SetField("bdg_area", shapeArea * numFloors)
#     layer.SetFeature(row)
# print "Calculated building area."

# for some reason, when the above adding field functions are not commented out, the stuff below doesn't run; when it is commented out, the below runs just fine.
# my guess is it has something to do with the way "layer" is used to refer to the input data in both cases.

# then, use dictionaries to input proportion of each use for each building type... multiply by that amount and put into appropriate field
for building in layer:
    # residential area
    for id, prop in propRes.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('res_area', propRes[id] * bldgArea)
            layer.SetFeature(building)
    # office area
    for id, prop in propOff.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('off_area', propOff[id] * bldgArea)
            layer.SetFeature(building)
    # retail area
    for id, prop in propRet.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('ret_area', propRet[id] * bldgArea)
            layer.SetFeature(building)
    # public assembly area
    for id, prop in propPa.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('pa_area', propPa[id] * bldgArea)
            layer.SetFeature(building)
    # garage area
    for id, prop in propGar.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('gar_area', propGar[id] * bldgArea)
            layer.SetFeature(building)
    # industrial area
    for id, prop in propFac.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('fac_area', propFac[id] * bldgArea)
            layer.SetFeature(building)
    # transportation area
    for id, prop in propTrans.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('trans_area', propTrans[id] * bldgArea)
            layer.SetFeature(building)
    # hotel area
    for id, prop in propHot.iteritems():
        if int(building.GetField('ide_eco')) == id:
            bldgArea = float(building.GetField('bdg_area'))
            layer.SetFeature(building)
            building.SetField('hot_area', propHot[id] * bldgArea)
            layer.SetFeature(building)

# I think the above could be simplified if all dictionaries were combined {1{1: 0}...} and the iterator was set up as such:
# for use, id, prop in useDict:
#   for use in useDict:
#       if int(building.GetField('ide_eco')) == id:
# etc, same as implemented, except this would involve mapping the different field types to the different uses, and really isn't necessary given what I'm trying to do here.

print "Calculated use by area."

# remember to save layer!

print "Completed in ", time.time()-start, " seconds."