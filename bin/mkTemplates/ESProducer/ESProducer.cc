// -*- C++ -*-
//
// Package:    __name__
// Class:      __class__
// 
/**\class __class__ __class__.h __subsys__/__class__/src/__class__.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  __author__
//         Created:  __date__
// __rcsid__
//
//


// system include files
#include <memory>
#include "boost/shared_ptr.hpp"

// user include files
#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/ESProducts.h"


//
// class declaration
//

class __class__ : public edm::ESProducer {
   public:
      __class__(const edm::ParameterSet&);
      ~__class__();

#python_begin
    datatypes = []
    for dtype in __datatypes__:
        datatypes.append("boost::shared_ptr<%s>" % dtype)
    return "      typedef edm::ESProducts<%s> ReturnType;" % ','.join(datatypes)
#python_end

      ReturnType produce(const __record__&);
   private:
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
   //the following line is needed to tell the framework what
   // data is being produced
   setWhatProduced(this);

   //now do what ever other initialization is needed
}


__class__::~__class__()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
__class__::ReturnType
__class__::produce(const __record__& iRecord)
{
   using namespace edm::es;
#python_begin
    out1 = []
    out2 = []
    for dtype in __datatypes__:
        out1.append("   boost::shared_ptr<%s> p%s;\n" % (dtype, dtype))
        out2.append("p%s" % dtype)
    output  = '\n'.join(out1)
    output += "   return products(%s);\n" % ','.join(out2)
    return output
#python_end

}

//define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(__class__);