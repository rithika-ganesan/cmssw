// ROOT script 

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void makeTrackPlots(TString inputRootFile = "L1TrkNtuple",
                    TString inputDir = "./") {

    // options 

    gROOT->SetBatch();
    gErrorIgnoreLevel = kWarning;
    cout.setf(ios::fixed);
    cout.precision(2);

    // get tree
    TChain* tree = new TChain("L1TrackNtuple/eventTree");
    tree->Add(inputDir + inputRootFile + ".root");

    if (tree->GetEntries() == 0) {
        cerr << "Input file doesn't exist or is empty, returning..." << endl;
        return;
    } 

    // set up variables
    vector<float>* tp_pt;
    vector<int>* tp_eventid; 
    vector<int>* tp_pdgid; 

    // set pointer to 0 / nullptr before passing to SetBranchAddress
    tp_pt = 0; 
    tp_eventid = 0;
    tp_pdgid = nullptr; 

    tree->SetBranchAddress("tp_pt", &tp_pt);
    tree->SetBranchAddress("tp_eventid", &tp_eventid);
    tree->SetBranchAddress("tp_pdgid", &tp_pdgid);



    // ----------------------
    //       event loop
    // ----------------------

    int nevt = tree->GetEntries(); 
    cout << "There are " << nevt << " events." << endl;
    for (int i = 0; i < 1; i++) {
        tree->GetEntry(i, 0); 

        // loop tracking particles
        for (int ip = 0; ip < (int)tp_pt->size(); ip++) {
            cout << "Event ID: " << tp_eventid->at(ip) << ", PDG ID: " << tp_pdgid->at(ip) << endl;
        }
    }

}