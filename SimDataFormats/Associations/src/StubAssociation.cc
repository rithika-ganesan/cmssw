#include "SimDataFormats/Associations/interface/StubAssociation.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "DataFormats/L1TrackTrigger/interface/TTStub.h"

#include <vector>
#include <deque>

namespace tt {

  // insert a TPPtr and its associated collection of TTstubRefs into the underlayering maps
  void StubAssociation::insert(const TPPtr& tpPtr, const std::vector<TTStubRef>& ttSTubRefs) {
    mapTPPtrsTTStubRefs_.insert({tpPtr, ttSTubRefs});
    // edm::LogVerbatim("Tracklet") << "mycheck for stubassociation";

    for (const TTStubRef& ttSTubRef : ttSTubRefs) {
      mapTTStubRefsTPPtrs_[ttSTubRef].push_back(tpPtr);

      if (ttSTubRef.isNonnull() && tpPtr.isNonnull()) {
        const auto& innerCluster = ttSTubRef->clusterRef(0);
        const auto& outerCluster = ttSTubRef->clusterRef(1);
        const auto mpIn  = innerCluster->findAverageLocalCoordinates();
        const auto mpOut = outerCluster->findAverageLocalCoordinates();

        edm::LogVerbatim("Tracklet")
            << "TRUTHSTUBINFO"
            << " tpKey=" << tpPtr.key()
            << " tpEvent=" << tpPtr->eventId().event()
            << " tpProd=" << tpPtr.id().productIndex()
            << " tpPdgId=" << tpPtr->pdgId()
            << " tpPt=" << tpPtr->pt()
            << " stubKey=" << ttSTubRef.key()
            << " stubKey=" << ttSTubRef.key()
            << " innerRow=" << mpIn.x()  << " innerCol=" << mpIn.y()
            << " outerRow=" << mpOut.x() << " outerCol=" << mpOut.y()
            << " innerKey=" << innerCluster.key() << " outerKey=" << outerCluster.key()
            << " detId=" << ttSTubRef->getDetId().rawId()
            << " bendFE=" << ttSTubRef->bendFE()
            << " bendBE=" << ttSTubRef->bendBE()
            << " rawBend=" << ttSTubRef->rawBend()
            << " innerClusterSize=" << (innerCluster.isNonnull() ? innerCluster->getHits().size() : 0)
            << " outerClusterSize=" << (outerCluster.isNonnull() ? outerCluster->getHits().size() : 0)
            << " innerClusterPos=" << ttSTubRef->innerClusterPosition()
            << " moduleTypePS=" << ttSTubRef->moduleTypePS();
      }
    }
  }

  // returns collection of TPPtrs associated to given TTstubRef
  const std::vector<TPPtr>& StubAssociation::findTrackingParticlePtrs(const TTStubRef& ttStubRef) const {
    const auto it = mapTTStubRefsTPPtrs_.find(ttStubRef);
    return it != mapTTStubRefsTPPtrs_.end() ? it->second : emptyTPPtrs_;
  }

  // returns collection of TTStubRefs associated to given TPPtr
  const std::vector<TTStubRef>& StubAssociation::findTTStubRefs(const TPPtr& tpPtr) const {
    const auto it = mapTPPtrsTTStubRefs_.find(tpPtr);
    return it != mapTPPtrsTTStubRefs_.end() ? it->second : emptyTTStubRefs_;
  }

}  // namespace tt
