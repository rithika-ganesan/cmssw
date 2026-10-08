import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('/afs/cern.ch/user/r/rganesan/private/plotting/classic.mplstyle')
plt.rcParams.update({"text.usetex": False})

# options
path = 'ttbarTracksOutputs.csv'
colnames = ['Event', 'Sector', 'Track', 'Layer', 'SeedLayer0', 'SeedLayer1', 'StubID']
ncms = 32
nlayers = 11
minidenticalstubs=3
debug_prints=True
debug_prints=False

# some functions
def adjust_column(col):
    return np.where(col > 6, col + 4, col)

def layer_number_corrections(df, colname='Layer'):
    df[colname] += 1 # shift layer values up by one so they read 1-11 instead of 0-10
    df[colname] = adjust_column(df[colname])
    return df

# get values
df = pd.read_csv(path, names=colnames, sep=',')
df = layer_number_corrections(df)
listEvents = np.unique(df['Event'])
listSectors = np.unique(df['Sector'])
listLayers = np.unique(df['Layer'])

# # sanity prints
# print("Event:", np.unique(df['Event']))
# print("Sector:", np.unique(df['Sector']))
# # print("Track:", np.unique(df['Track']))
# print("Layer:", np.unique(df['Layer']))
# print("SeedLayer0:", np.unique(df['SeedLayer0']))
# print("SeedLayer1:", np.unique(df['SeedLayer1']))
# # print("StubID:", np.unique(df['StubID']))

# format data
events = {}

# start loop
n_stubs_per_track = []
# print(f"Running over {len(listEvents)} events.")
# loop over events
for ev in listEvents:
    events[ev] = {}
    print(" ")
    # loop over sectors
    for sector in listSectors: 
        events[ev][sector] = []

        tmp_ = df[df['Event'] == ev]
        stream = tmp_[tmp_['Sector'] == sector]
        sizeTracks = len(np.unique(stream['Track']))

        if debug_prints:
            ev_ = np.unique(stream['Event'])[0]
            sector_ = np.unique(stream['Sector'])[0]
            print(f"For event {ev_}, sector {sector_}: running over {sizeTracks} tracks")

        # loop over tracks
        for track in range(sizeTracks):
            stubs_ = stream[stream['Track'] == track].drop(['Event', 'Sector', 'Track'], axis=1)
            n_stubs_per_track.append(len(stubs_))

            # check that all entries for the track have the same seed layers:
            sl0 = np.unique(stubs_['SeedLayer0'])
            sl1 = np.unique(stubs_['SeedLayer1'])
            if len(sl0) != 1 or len(sl1) != 1:
                raise ValueError("Seed layers for a single track are different across stub entries.")
            seedLayers_ = [sl0[0], sl1[0]]
            
            # get stub and layers: 
            orderedStubs_ = []
            for ilayer in listLayers:
                layer = stubs_[stubs_['Layer'] == ilayer]
                if len(layer) > 1:
                    raise ValueError("More than one stub in a layer.")
                elif len(layer) == 1:
                    layerStubVal = layer['StubID'].to_list()[0]
                else:
                    layerStubVal = None
                orderedStubs_.append(layerStubVal)

            track_ = {
                'seedlayers': seedLayers_,
                'stubs': orderedStubs_
            }

            events[ev][sector].append(track_)



def equalEnough(t0, t1):
    same=0
    for layer in range(nlayers):
        s0 = t0['stubs'][layer]
        s1 = t1['stubs'][layer]
        if s0 and s1 and s0==s1:
            same += 1
    return same >= minidenticalstubs

# def equalEnough(t0, t1):
#     same=0
#     for layer in range(nlayers):
#         s0 = t0['stubs'][layer]
#         s1 = t1['stubs'][layer]
#         if s0 and s1:
#             if s0 == s1:
#                 same += 1
#             elif np.abs( (s0 - s1) / ((s0 + s1)/2)) < 0.04:
#                 same += 0.5
#     return same >= minidenticalstubs


def compareAllTracks(ev, sector):
    tracks_ = events[ev][sector]
    pairs = []

    ntracks = len(tracks_)

    for i0, track0 in enumerate(tracks_):
        for i1, track1 in enumerate(tracks_):
            if i1 > i0:
                if equalEnough(track0, track1) == True:
                    print([i0, i1])
                    pairs.append([i0, i1])

    return pairs

# compareAllTracks(0, 0)


# def getTruthVals(ev, sector):
#     tracks_ = events[ev][sector]
#     pairs = []

#     ntracks = len(tracks_)

#     for i0, track0 in enumerate(tracks_):
#         for i1, track1 in enumerate(tracks_):
#             if i1 > i0:
#                 if equalEnough(track0, track1) == True:
#                     pairs.append([i0, i1])

#     pairs = np.array(pairs)

#     trackindices = []
#     tracks = []
#     for i in range(ntracks):
#         if i not in pairs.flatten():
#             print(f"Track {i} has no duplicates.")
#             trackindices.append(i)
#             tracks.append([i])
#         elif i in pairs.T[0]:
#             if i not in trackindices: 
#                 idupes = [i]
#                 imatches = pairs[np.argwhere(pairs.T[0]==i).T[0]].T[1].tolist()
#                 print(f"Track {i} has the following matches.")
#                 for sv in imatches:
#                     if sv in pairs.T[0]:
#                         print(sv, )
#             else:
#                 print(f"Pause on track {i}.")

#     return None



# getTruthVals(0, 0)
# flattenPairs(0, 0)





def compareNew(ev, sector):
    allTracks = events[ev][sector]

    cms = [None] * 32
    cmstrackid = [None] * 32

    for i in range(len(allTracks)):
        track = allTracks[i]
        # print(f"\nFor track {i}:")
        for j, cm in enumerate(cms):   
            if cm == None and track != None:
                cmstrackid[j], cms[j] = i, track
                # print(f"CM {j} is currently empty. We fill it with track {i} and move on to the next track.")      
                break
            else: 
                # print(f"CM {j} is occupied by track {cmstrackid[j]}.")
                result = equalEnough(cm, track)
                if result == True:
                    # print(f"Tracks {i} and {cmstrackid[j]} are considered equal enough. Track {i} is set to null.")
                    allTracks[i] = None
                    break

    outputTrackIndices = []
    for i, a in enumerate(allTracks):
        if a != None:
            outputTrackIndices.append(i)

    return allTracks, outputTrackIndices

# allTracks, outputTrackIndices = compareNew(0, 0)
# print(outputTrackIndices)


def compareMatchedTracks(ev=0, sector=0, indices=[1, 3, 4, 11, 14, 17, 24, 27, 35, 41]):
    allTracks = events[ev][sector]

    myTracks = []
    for ind in indices:
        myTracks.append(allTracks[ind])
        print(allTracks[ind])

    return None

compareMatchedTracks()





        



            
        

    