
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()

#pathin_ = 'root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V24/singlesys_22_test_v5/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1.root'
#pathin_ = 'root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V24/TEST/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1.root'
#pathin_ = 'root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V24/TEST/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/tree_VHBB_HEPPY_V24_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0_ext1-v1_70_1bd625da610d27dc2fec62bfc9ac74b33588f1fba2e6441645fd9c51.root'
pathin_ = 'root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V24/TEST2/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1.root'

f = ROOT.TFile.Open(pathin_)
t = f.Get("tree")


VarList = ['HCSV_reg_corrSYSUD_mass_CAT','HCSV_reg_corrSYSUD_pt_CAT', 'HCSV_reg_corrSYSUD_eta_CAT', 'HCSV_reg_corrSYSUD_phi_CAT','Jet_pt_reg_corrSYSUD_CAT_INDEX0','Jet_pt_reg_corrSYSUD_CAT_INDEX1', 'Sum$(Jet_pt_reg_corrSYSUD_CAT>30&&abs(Jet_eta)<2.4&&Jet_puId==7&&Jet_id>0&&aJCidx!=(hJCidx[0])&&(aJCidx!=(hJCidx[1])))']
SysList = ['JER','JEC']
UDList = ['Up','Down']
CatList = ['HighCentral','LowCentral','HighForward','LowForward']
AxisList = {'mass':[20,0,400],'HCSV_reg_pt':[20,0,400],'phi':[20,-3.2, 3.2],'eta':[20,0,5],'Jet_pt':[20,0,300]}
for var in VarList:
    for syst in SysList:
        for cat in CatList:
            c = ROOT.TCanvas('c','c',800,800) 
            pad1 = ROOT.TPad('pad1','pad1', 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0)
            pad1.SetGridx()
            pad1.Draw()
            pad1.cd()

            nbin = 0
            xmin = 0
            xmax = 0
            var_nom = var.replace('SYSUD','').replace('_CAT','').replace('_corr','')
            for axis in AxisList:
                if axis in var_nom:
                    nbin = AxisList[axis][0]
                    xmin = AxisList[axis][1]
                    xmax = AxisList[axis][2]

            h_nom = ROOT.TH1D('h_nom','h_nom',nbin, xmin, xmax)
            print 'var nom is', var_nom
            if 'Jet_pt' in var_nom:
                if '_INDEX0'in var_nom: t.Draw(var_nom.replace('_INDEX0','[hJCidx[0]]')+'>>h_nom')
                elif '_INDEX1'in var_nom: t.Draw(var_nom.replace('_INDEX1','[hJCidx[1]]')+'>>h_nom')
            else:
                t.Draw(var_nom+'>>h_nom')
            h_nom.SetLineColor(1)
            h_nom.SetMarkerStyle(20)
            h_nom.SetMarkerColor(1)
            h_nom.SetLineWidth(2)
            h_nom.Sumw2()

            h_ud = {} 
            for ud in UDList:
                #fill Dic
                SysDic = {}
                SysDic['var'] = var 
                SysDic['sys'] = syst
                SysDic['UD'] = ud 
                SysDic['cat'] = cat 
                SysDic['varname'] = var.replace('SYS',syst).replace('UD',ud).replace('CAT',cat)
                h_ud[ud] = ROOT.TH1D('h_%s'%ud,'h_%s'%ud,nbin, xmin, xmax)
                if 'Jet_pt' in SysDic['varname']:
                    if '_INDEX0'in SysDic['varname']: 
                        t.Draw(SysDic['varname'].replace('_INDEX0','[hJCidx[0]]')+'>>h_%s'%ud)
                    elif '_INDEX1'in SysDic['varname']: 
                        t.Draw(SysDic['varname'].replace('_INDEX1','[hJCidx[1]]')+'>>h_%s'%ud)
                else:
                    t.Draw(SysDic['varname']+'>>h_%s'%ud)
                #h_ud[ud].Draw('same')
                #t.Draw(SysDic['varname'])

            h_nom.Draw()
            h_nom.GetXaxis().SetTitle(var_nom)
            h_ud['Up'].Draw('same')
            h_ud['Up'].SetLineColor(4)
            h_ud['Up'].SetLineStyle(4)
            h_ud['Up'].SetLineWidth(2)
            h_ud['Up'].GetYaxis().SetNdivisions(505)
            h_ud['Up'].GetYaxis().SetTitleSize(20)
            h_ud['Up'].GetYaxis().SetTitleFont(43)
            h_ud['Up'].GetYaxis().SetTitleOffset(1.55)
            h_ud['Up'].GetYaxis().SetLabelFont(43)
            h_ud['Up'].GetYaxis().SetLabelSize(15)
            h_ud['Up'].GetXaxis().SetTitleSize(20)
            h_ud['Up'].GetXaxis().SetTitleFont(43)
            h_ud['Up'].GetXaxis().SetTitleOffset(4.)
            h_ud['Up'].GetXaxis().SetLabelFont(43)
            h_ud['Up'].GetXaxis().SetLabelSize(15)
            h_ud['Up'].GetXaxis().SetTitle(var_nom)

            h_ud['Down'].Draw('same')
            h_ud['Down'].SetLineColor(2)
            h_ud['Down'].SetLineStyle(2)
            h_ud['Down'].SetLineWidth(2)


            leg = ROOT.TLegend(0.7, 0.8, 1 , 1)
            leg.AddEntry(h_nom,'nominal')
            leg.AddEntry(h_ud['Up'],'up')
            leg.AddEntry(h_ud['Down'],'down')
            leg.Draw('same')

            c.cd()
            pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.2)
            pad2.SetGridx()
            pad2.SetGridy()
            pad2.Draw()
            pad2.cd()

            ratio_up =  h_ud['Up'].Clone()
            ratio_up.Divide(h_nom) 
            ratio_up.Draw()
            ratio_up.GetYaxis().SetRangeUser(0.9,1.1)
            ratio_down =  h_ud['Down'].Clone()
            ratio_down.Divide(h_nom) 
            ratio_down.Draw('same')

            c.SaveAs('BtagSplitNumUpDown/'+SysDic['varname']+'.pdf')
            c.SaveAs('BtagSplitNumUpDown/'+SysDic['varname']+'.png')
            c.SaveAs('BtagSplitNumUpDown/'+SysDic['varname']+'.root')
            c.SaveAs('BtagSplitNumUpDown/'+SysDic['varname']+'.C')

