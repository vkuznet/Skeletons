// -*- C++ -*-
//
// Package:    __class__
// Class:      __class__
// 
/**\class __class__ __class__.cc __subsys__/__class__/src/__class__.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  John Doe
//         Created:  day-mon-xx
// RCS(Id)
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//
// class declaration
//

class __class__ : public edm::EDFilter {
   public:
      explicit __class__(const edm::ParameterSet&);
      ~__class__();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      //virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      //virtual bool endRun(edm::Run&, edm::EventSetup const&);
      //virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      //virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
__class__::__class__(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

}


__class__::~__class__()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
__class__::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
   return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
__class__::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
__class__::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
bool
__class__::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
bool
__class__::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
bool
__class__::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
bool
__class__::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
__class__::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(__class__);
