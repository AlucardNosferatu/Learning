/*
 * Untitled2.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on Mar 9 2021, 17:14 by COMSOL 5.0.0.243. */
public class Untitled2 {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model.modelPath("C:\\Users\\16413\\Desktop\\FFCS\\TEMP");

    model.modelNode().create("comp1");

    model.geom().create("geom1", 3);

    model.mesh().create("mesh1", "geom1");

    model.physics().create("spf", "LaminarFlow", "geom1");
    model.physics("spf").prop("AdvancedSettingProperty").set("UsePseudoTime", "1");
    model.physics().create("ht", "HeatTransfer", "geom1");
    model.physics("ht").prop("ShapeProperty").set("order_temperature", "1");
    model.physics("ht").create("fluid1", "FluidHeatTransferModel");
    model.physics("ht").feature("fluid1").selection().all();
    model.physics().create("ht2", "HeatTransferInFluids", "geom1");

    model.multiphysics().create("nitf1", "NonIsothermalFlow", "geom1", 3);
    model.multiphysics("nitf1").set("Fluid_physics", "spf");
    model.multiphysics("nitf1").set("Heat_physics", "ht");

    model.study().create("std1");
    model.study("std1").create("time", "Transient");
    model.study("std1").feature("time").activate("spf", true);
    model.study("std1").feature("time").activate("ht", true);
    model.study("std1").feature("time").activate("ht2", true);

    model.geom("geom1").create("imp1", "Import");
    model.geom("geom1").feature("imp1").set("type", "cad");
    model.geom("geom1").feature("imp1").set("filename", "C:\\Users\\16413\\Desktop\\BOX.SLDPRT");
    model.geom("geom1").feature("imp1").set("unit", "source");
    model.geom("geom1").run("");
    model.geom("geom1").feature("imp1").set("filename", "C:\\Users\\16413\\Desktop\\BOX.STEP");
    model.geom("geom1").feature("imp1").importData();
    model.geom("geom1").run("imp1");
    model.geom("geom1").feature().create("rev1", "Revolve");
    model.geom("geom1").feature("rev1").selection("input").init();
    model.geom("geom1").feature("rev1").selection("input").set(new String[]{});
    model.geom("geom1").feature("rev1").selection("inputface").set("imp1", new int[]{4});
    model.geom("geom1").feature("rev1").selection("inputface").clear("imp1");
    model.geom("geom1").feature("rev1").selection("inputface").set("imp1", new int[]{5});
    model.geom("geom1").feature().remove("rev1");
    model.geom("geom1").run("imp1");
    model.geom("geom1").create("rot1", "Rotate");
    model.geom("geom1").feature("rot1").selection("input").set(new String[]{"imp1"});
    model.geom("geom1").feature("rot1").set("axistype", "x");
    model.geom("geom1").feature("rot1").set("rot", "90");
    model.geom("geom1").run("rot1");
    model.geom("geom1").run("rot1");
    model.geom("geom1").run();

    model.material().create("mat1", "Common", "comp1");
    model.material("mat1").label("Concrete");
    model.material("mat1").set("family", "concrete");
    model.material("mat1").propertyGroup("def").set("thermalexpansioncoefficient", "10e-6[1/K]");
    model.material("mat1").propertyGroup("def").set("density", "2300[kg/m^3]");
    model.material("mat1").propertyGroup("def").set("thermalconductivity", "1.8[W/(m*K)]");
    model.material("mat1").propertyGroup("def").set("heatcapacity", "880[J/(kg*K)]");
    model.material("mat1").propertyGroup().create("Enu", "\u6768\u6c0f\u6a21\u91cf\u548c\u6cca\u677e\u6bd4");
    model.material("mat1").propertyGroup("Enu").set("poissonsratio", "0.33");
    model.material("mat1").propertyGroup("Enu").set("youngsmodulus", "25e9[Pa]");
    model.material("mat1").set("family", "concrete");
    model.material("mat1").selection().set(new int[]{1});
    model.material("mat1").selection().all();
    model.material().create("mat2", "Common", "comp1");
    model.material("mat2").label("Air");
    model.material("mat2").set("family", "air");
    model.material("mat2").propertyGroup("def").set("relpermeability", "1");
    model.material("mat2").propertyGroup("def").set("relpermittivity", "1");
    model.material("mat2").propertyGroup("def").set("dynamicviscosity", "eta(T[1/K])[Pa*s]");
    model.material("mat2").propertyGroup("def").set("ratioofspecificheat", "1.4");
    model.material("mat2").propertyGroup("def").set("electricconductivity", "0[S/m]");
    model.material("mat2").propertyGroup("def").set("heatcapacity", "Cp(T[1/K])[J/(kg*K)]");
    model.material("mat2").propertyGroup("def").set("density", "rho(pA[1/Pa],T[1/K])[kg/m^3]");
    model.material("mat2").propertyGroup("def").set("thermalconductivity", "k(T[1/K])[W/(m*K)]");
    model.material("mat2").propertyGroup("def").set("soundspeed", "cs(T[1/K])[m/s]");
    model.material("mat2").propertyGroup("def").func().create("eta", "Piecewise");
    model.material("mat2").propertyGroup("def").func("eta").set("funcname", "eta");
    model.material("mat2").propertyGroup("def").func("eta").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("eta").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("eta")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-8.38278E-7+8.35717342E-8*T^1-7.69429583E-11*T^2+4.6437266E-14*T^3-1.06585607E-17*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("Cp", "Piecewise");
    model.material("mat2").propertyGroup("def").func("Cp").set("funcname", "Cp");
    model.material("mat2").propertyGroup("def").func("Cp").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("Cp").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("Cp")
         .set("pieces", new String[][]{{"200.0", "1600.0", "1047.63657-0.372589265*T^1+9.45304214E-4*T^2-6.02409443E-7*T^3+1.2858961E-10*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("rho", "Analytic");
    model.material("mat2").propertyGroup("def").func("rho").set("funcname", "rho");
    model.material("mat2").propertyGroup("def").func("rho").set("args", new String[]{"pA", "T"});
    model.material("mat2").propertyGroup("def").func("rho").set("expr", "pA*0.02897/8.314/T");
    model.material("mat2").propertyGroup("def").func("rho").set("dermethod", "manual");
    model.material("mat2").propertyGroup("def").func("rho")
         .set("argders", new String[][]{{"pA", "d(pA*0.02897/8.314/T,pA)"}, {"T", "d(pA*0.02897/8.314/T,T)"}});
    model.material("mat2").propertyGroup("def").func().create("k", "Piecewise");
    model.material("mat2").propertyGroup("def").func("k").set("funcname", "k");
    model.material("mat2").propertyGroup("def").func("k").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("k").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("k")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-0.00227583562+1.15480022E-4*T^1-7.90252856E-8*T^2+4.11702505E-11*T^3-7.43864331E-15*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("cs", "Analytic");
    model.material("mat2").propertyGroup("def").func("cs").set("funcname", "cs");
    model.material("mat2").propertyGroup("def").func("cs").set("args", new String[]{"T"});
    model.material("mat2").propertyGroup("def").func("cs").set("expr", "sqrt(1.4*287*T)");
    model.material("mat2").propertyGroup("def").func("cs").set("dermethod", "manual");
    model.material("mat2").propertyGroup("def").func("cs")
         .set("argders", new String[][]{{"T", "d(sqrt(1.4*287*T),T)"}});
    model.material("mat2").propertyGroup("def").addInput("temperature");
    model.material("mat2").propertyGroup("def").addInput("pressure");
    model.material("mat2").propertyGroup().create("RefractiveIndex", "\u6298\u5c04\u7387");
    model.material("mat2").propertyGroup("RefractiveIndex").set("n", "1");
    model.material("mat2").set("family", "air");
    model.material("mat2").selection().geom("geom1", 2);
    model.material("mat2").selection().set(new int[]{12});
    model.material("mat2").selection().all();
    model.material("mat2").selection().set(new int[]{});
    model.material("mat2").selection().geom("geom1", 3);
    model.material("mat2").selection().set(new int[]{1});
    model.material("mat1").selection().set(new int[]{});
    model.material("mat1").selection().geom("geom1", 2);
    model.material("mat1").selection().geom("geom1", 1);
    model.material("mat1").selection().geom("geom1", 3);
    model.material("mat1").selection().all();
    model.material().remove("mat2");
    model.material().create("mat2", "Common", "comp1");
    model.material("mat2").label("Air");
    model.material("mat2").set("family", "air");
    model.material("mat2").propertyGroup("def").set("relpermeability", "1");
    model.material("mat2").propertyGroup("def").set("relpermittivity", "1");
    model.material("mat2").propertyGroup("def").set("dynamicviscosity", "eta(T[1/K])[Pa*s]");
    model.material("mat2").propertyGroup("def").set("ratioofspecificheat", "1.4");
    model.material("mat2").propertyGroup("def").set("electricconductivity", "0[S/m]");
    model.material("mat2").propertyGroup("def").set("heatcapacity", "Cp(T[1/K])[J/(kg*K)]");
    model.material("mat2").propertyGroup("def").set("density", "rho(pA[1/Pa],T[1/K])[kg/m^3]");
    model.material("mat2").propertyGroup("def").set("thermalconductivity", "k(T[1/K])[W/(m*K)]");
    model.material("mat2").propertyGroup("def").set("soundspeed", "cs(T[1/K])[m/s]");
    model.material("mat2").propertyGroup("def").func().create("eta", "Piecewise");
    model.material("mat2").propertyGroup("def").func("eta").set("funcname", "eta");
    model.material("mat2").propertyGroup("def").func("eta").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("eta").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("eta")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-8.38278E-7+8.35717342E-8*T^1-7.69429583E-11*T^2+4.6437266E-14*T^3-1.06585607E-17*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("Cp", "Piecewise");
    model.material("mat2").propertyGroup("def").func("Cp").set("funcname", "Cp");
    model.material("mat2").propertyGroup("def").func("Cp").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("Cp").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("Cp")
         .set("pieces", new String[][]{{"200.0", "1600.0", "1047.63657-0.372589265*T^1+9.45304214E-4*T^2-6.02409443E-7*T^3+1.2858961E-10*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("rho", "Analytic");
    model.material("mat2").propertyGroup("def").func("rho").set("funcname", "rho");
    model.material("mat2").propertyGroup("def").func("rho").set("args", new String[]{"pA", "T"});
    model.material("mat2").propertyGroup("def").func("rho").set("expr", "pA*0.02897/8.314/T");
    model.material("mat2").propertyGroup("def").func("rho").set("dermethod", "manual");
    model.material("mat2").propertyGroup("def").func("rho")
         .set("argders", new String[][]{{"pA", "d(pA*0.02897/8.314/T,pA)"}, {"T", "d(pA*0.02897/8.314/T,T)"}});
    model.material("mat2").propertyGroup("def").func().create("k", "Piecewise");
    model.material("mat2").propertyGroup("def").func("k").set("funcname", "k");
    model.material("mat2").propertyGroup("def").func("k").set("arg", "T");
    model.material("mat2").propertyGroup("def").func("k").set("extrap", "constant");
    model.material("mat2").propertyGroup("def").func("k")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-0.00227583562+1.15480022E-4*T^1-7.90252856E-8*T^2+4.11702505E-11*T^3-7.43864331E-15*T^4"}});
    model.material("mat2").propertyGroup("def").func().create("cs", "Analytic");
    model.material("mat2").propertyGroup("def").func("cs").set("funcname", "cs");
    model.material("mat2").propertyGroup("def").func("cs").set("args", new String[]{"T"});
    model.material("mat2").propertyGroup("def").func("cs").set("expr", "sqrt(1.4*287*T)");
    model.material("mat2").propertyGroup("def").func("cs").set("dermethod", "manual");
    model.material("mat2").propertyGroup("def").func("cs")
         .set("argders", new String[][]{{"T", "d(sqrt(1.4*287*T),T)"}});
    model.material("mat2").propertyGroup("def").addInput("temperature");
    model.material("mat2").propertyGroup("def").addInput("pressure");
    model.material("mat2").propertyGroup().create("RefractiveIndex", "\u6298\u5c04\u7387");
    model.material("mat2").propertyGroup("RefractiveIndex").set("n", "1");
    model.material("mat2").set("family", "air");
    model.material().move("mat2", 0);
    model.material("mat2").selection().set(new int[]{});
    model.material("mat2").selection().all();
    model.material("mat2").selection().geom("geom1", 2);
    model.material("mat2").selection().all();
    model.material("mat2").selection().set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12});
    model.material("mat2").selection().geom("geom1", 3);
    model.material("mat2").selection().all();
    model.material("mat2").selection().set(new int[]{});

    model.view("view1").hideObjects().clear();
    model.view("view1").hideEntities().clear();
    model.view("view1").set("geomhidestatus", "ignore");

    model.geom("geom1").run("imp1");
    model.geom("geom1").run("rot1");

    model.material("mat1").selection().set(new int[]{});
    model.material("mat2").selection().set(new int[]{1});
    model.material("mat1").selection().set(new int[]{});
    model.material("mat1").selection().geom("geom1", 2);
    model.material("mat1").selection().set(new int[]{6, 7, 8, 9, 10, 11});

    model.physics("ht").feature().create("open1", "OpenBoundary", 2);
    model.physics("ht").feature().remove("open1");
    model.physics("ht").feature().create("ofl1", "ConvectiveOutflow", 2);
    model.physics("ht").feature().remove("ofl1");
    model.physics("ht").feature().create("hf1", "HeatFluxBoundary", 2);
    model.physics("ht").feature("hf1").selection().set(new int[]{6, 7, 8, 9, 10, 11});
    model.physics("ht2").active(false);

    model.geom("geom1").run("rot1");
    model.geom("geom1").create("sph1", "Sphere");
    model.geom("geom1").run("sph1");
    model.geom("geom1").run("sph1");
    model.geom("geom1").create("mov1", "Move");
    model.geom("geom1").feature("mov1").selection("input").set(new String[]{"sph1"});
    model.geom("geom1").feature("mov1").set("displx", "10");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature("mov1").set("disply", "10");
    model.geom("geom1").feature("mov1").set("displz", "5");
    model.geom("geom1").run("mov1");
    model.geom("geom1").run();

    model.material().create("mat3", "Common", "comp1");
    model.material("mat3").label("Iron");
    model.material("mat3").set("family", "iron");
    model.material("mat3").propertyGroup("def").set("relpermeability", "4000");
    model.material("mat3").propertyGroup("def").set("electricconductivity", "1.12e7[S/m]");
    model.material("mat3").propertyGroup("def").set("thermalexpansioncoefficient", "12.2e-6[1/K]");
    model.material("mat3").propertyGroup("def").set("heatcapacity", "440[J/(kg*K)]");
    model.material("mat3").propertyGroup("def").set("relpermittivity", "1");
    model.material("mat3").propertyGroup("def").set("density", "7870[kg/m^3]");
    model.material("mat3").propertyGroup("def").set("thermalconductivity", "76.2[W/(m*K)]");
    model.material("mat3").propertyGroup().create("Enu", "\u6768\u6c0f\u6a21\u91cf\u548c\u6cca\u677e\u6bd4");
    model.material("mat3").propertyGroup("Enu").set("poissonsratio", "0.29");
    model.material("mat3").propertyGroup("Enu").set("youngsmodulus", "200e9[Pa]");
    model.material("mat3").set("family", "iron");
    model.material("mat3").selection().set(new int[]{2});

    model.physics("ht").feature("hf1").selection().set(new int[]{6, 7, 8, 9, 10, 11, 19});

    model.material("mat2").selection().set(new int[]{1});
    model.material("mat2").selection().all();
    model.material("mat3").selection().geom("geom1", 2);
    model.material("mat3").selection().set(new int[]{12});
    model.material("mat1").selection().set(new int[]{});
    model.material("mat3").selection().set(new int[]{12});
    model.material("mat1").selection().set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20});

    model.physics("ht").feature("hf1").selection().set(new int[]{11, 12, 13, 14, 15, 16, 17, 18});

    model.material("mat3").selection().set(new int[]{});
    model.material().duplicate("mat4", "mat3");
    model.material().remove("mat4");
    model.material("mat3").selection().set(new int[]{11, 12, 13, 14, 15, 16, 17, 18});

    model.physics("ht").feature("hf1").selection().set(new int[]{6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19});
    model.physics("ht").feature().create("hs1", "HeatSource", 3);
    model.physics("ht").feature("hs1").selection().all();
    model.physics("ht").feature("hs1").selection().set(new int[]{2});
    model.physics("ht").feature("hs1").set("Q", "2500");

    model.study("std1").feature("time").set("tlist", "range(0,0.1,10)");

    model.sol().create("sol1");

    model.mesh("mesh1").run("cr1");

    model.study("std1").feature("time").set("plot", "on");

    model.sol().create("sol2");
    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "Default");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("i1", "Iterative");
    model.sol("sol2").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol2").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol2").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol2").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol2").feature("t1").feature("i1").set("maxlinit", 50);
    model.sol("sol2").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol2").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("prefun", "gmg");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("mcasegen", "any");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("gmglevels", 1);
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "i1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.result().create("pg1", "PlotGroup3D");
    model.result("pg1").label("\u901f\u5ea6 (spf)");
    model.result("pg1").set("data", "dset2");
    model.result("pg1").set("oldanalysistype", "noneavailable");
    model.result("pg1").set("frametype", "spatial");
    model.result("pg1").set("data", "dset2");
    model.result("pg1").feature().create("slc1", "Slice");
    model.result("pg1").feature("slc1").set("oldanalysistype", "noneavailable");
    model.result("pg1").feature("slc1").set("data", "parent");
    model.result().dataset().create("surf1", "Surface");
    model.result().dataset("surf1").selection().geom("geom1", 2);
    model.result().dataset("surf1").selection()
         .set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20});
    model.result().dataset("surf1").selection().inherit(false);
    model.result().dataset("surf1").set("data", "none");
    model.result().dataset().create("surf2", "Surface");
    model.result().dataset("surf2").selection().geom("geom1", 2);
    model.result().dataset("surf2").selection()
         .set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20});
    model.result().dataset("surf2").selection().inherit(false);
    model.result().dataset("surf2").set("data", "none");
    model.result().dataset("surf1").set("data", "dset2");
    model.result().dataset("surf1").selection().geom("geom1", 2);
    model.result().dataset("surf1").selection()
         .set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20});
    model.result().dataset("surf1").selection().inherit(false);
    model.result().dataset("surf2").set("data", "dset2");
    model.result().dataset("surf2").selection().geom("geom1", 2);
    model.result().dataset("surf2").selection()
         .set(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20});
    model.result().dataset("surf2").selection().inherit(false);
    model.result().create("pg2", "PlotGroup3D");
    model.result("pg2").label("\u538b\u529b (spf)");
    model.result("pg2").set("data", "dset2");
    model.result("pg2").set("oldanalysistype", "noneavailable");
    model.result("pg2").set("title", "Surface contour: Pressure (Pa)");
    model.result("pg2").set("frametype", "spatial");
    model.result("pg2").set("titletype", "auto");
    model.result("pg2").set("data", "dset2");
    model.result("pg2").feature().create("surf1", "Surface");
    model.result("pg2").feature("surf1").set("data", "surf1");
    model.result("pg2").feature("surf1").set("oldanalysistype", "noneavailable");
    model.result("pg2").feature("surf1").set("expr", "1");
    model.result("pg2").feature("surf1").set("titletype", "none");
    model.result("pg2").feature("surf1").set("isuniformshown", true);
    model.result("pg2").feature("surf1").set("isuniform", true);
    model.result("pg2").feature("surf1").set("coloring", "uniform");
    model.result("pg2").feature("surf1").set("color", "gray");
    model.result("pg2").feature("surf1").set("data", "surf1");
    model.result("pg2").feature().create("con1", "Contour");
    model.result("pg2").feature("con1").label("\u538b\u529b");
    model.result("pg2").feature("con1").set("data", "surf2");
    model.result("pg2").feature("con1").set("oldanalysistype", "noneavailable");
    model.result("pg2").feature("con1").set("expr", "p");
    model.result("pg2").feature("con1").set("number", 40);
    model.result("pg2").feature("con1").set("data", "surf2");
    model.result().create("pg3", "PlotGroup3D");
    model.result("pg3").label("\u6e29\u5ea6 (ht)");
    model.result("pg3").set("data", "dset2");
    model.result("pg3").set("oldanalysistype", "noneavailable");
    model.result("pg3").set("data", "dset2");
    model.result("pg3").feature().create("surf1", "Surface");
    model.result("pg3").feature("surf1").set("oldanalysistype", "noneavailable");
    model.result("pg3").feature("surf1").set("expr", "T");
    model.result("pg3").feature("surf1").set("colortable", "ThermalLight");
    model.result("pg3").feature("surf1").set("data", "parent");
    model.result().create("pg4", "PlotGroup3D");
    model.result("pg4").label("\u7b49\u6e29\u7ebf (ht)");
    model.result("pg4").set("data", "dset2");
    model.result("pg4").set("oldanalysistype", "noneavailable");
    model.result("pg4").set("data", "dset2");
    model.result("pg4").feature().create("iso1", "Isosurface");
    model.result("pg4").feature("iso1").set("oldanalysistype", "noneavailable");
    model.result("pg4").feature("iso1").set("expr", "T");
    model.result("pg4").feature("iso1").set("number", 10);
    model.result("pg4").feature("iso1").set("colortable", "ThermalLight");
    model.result("pg4").feature("iso1").set("data", "parent");
    model.result("pg1").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg3").run();
    model.result("pg3").run();
    model.result("pg4").run();
    model.result("pg4").run();
    model.result("pg1").run();

    model.physics("spf").selection().set(new int[]{1, 2});
    model.physics("spf").selection().all();
    model.physics("spf").feature().create("open1", "OpenBoundary", 2);
    model.physics("spf").feature().remove("open1");
    model.physics("spf").feature().create("iw1", "InteriorWall", 2);
    model.physics("spf").feature("iw1").selection().all();
    model.physics("spf").feature().remove("iw1");
    model.physics("spf").feature().create("vf1", "VolumeForce", 3);
    model.physics("spf").feature().remove("vf1");
    model.physics().move("spf", 1);
    model.physics().remove("ht2");
    model.physics("ht").feature().create("tc1", "ThermalContact", 2);

    model.cpl().remove("intExtBnd4");
    model.cpl().remove("intIntBnd4");
    model.cpl().remove("intBnd2");

    model.weak().remove("weak3");

    model.cpl().create("intExtBnd4", "Integration", "geom1");
    model.cpl("intExtBnd4").set("opname", "root.comp1.ht.hf1.intExtBnd");
    model.cpl("intExtBnd4").set("intorder", 4);
    model.cpl("intExtBnd4").set("frame", "material");
    model.cpl("intExtBnd4").label("root.comp1.ht.hf1.intExtBnd");
    model.cpl("intExtBnd4").set("method", "integration");
    model.cpl("intExtBnd4").selection().geom("geom1", 2);
    model.cpl("intExtBnd4").selection().set(new int[]{6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19});
    model.cpl("intExtBnd4").selection().inherit(false);
    model.cpl().create("intIntBnd4", "Integration", "geom1");
    model.cpl("intIntBnd4").set("opname", "root.comp1.ht.hf1.intIntBnd");
    model.cpl("intIntBnd4").set("intorder", 4);
    model.cpl("intIntBnd4").set("frame", "material");
    model.cpl("intIntBnd4").label("root.comp1.ht.hf1.intIntBnd");
    model.cpl("intIntBnd4").set("method", "integration");
    model.cpl("intIntBnd4").selection().geom("geom1", 2);
    model.cpl("intIntBnd4").selection().set(new int[]{});
    model.cpl("intIntBnd4").selection().inherit(false);
    model.cpl().create("intBnd2", "Integration", "geom1");
    model.cpl("intBnd2").set("opname", "root.comp1.ht.hf1.intBnd");
    model.cpl("intBnd2").set("intorder", 4);
    model.cpl("intBnd2").set("frame", "material");
    model.cpl("intBnd2").label("root.comp1.ht.hf1.intBnd");
    model.cpl("intBnd2").set("method", "integration");
    model.cpl("intBnd2").selection().geom("geom1", 2);
    model.cpl("intBnd2").selection().set(new int[]{6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19});
    model.cpl("intBnd2").selection().inherit(false);

    model.physics("ht").feature().move("tc1", 8);
    model.physics("ht").feature().move("tc1", 7);
    model.physics("ht").feature("hf1").active(false);
    model.physics("ht").feature().remove("tc1");
    model.physics("ht").feature("hf1").active(true);

    model.mesh("mesh1").autoMeshSize(6);
    model.mesh("mesh1").run();
    model.mesh("mesh1").autoMeshSize(7);
    model.mesh("mesh1").run();

    model.multiphysics("nitf1").set("SpecifyDensity", "FromHeatTransferInterface");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.geom("geom1").run("mov1");
    model.geom("geom1").create("blk1", "Block");

    return model;
  }

  public static Model run2(Model model) {
    model.geom("geom1").feature("blk1").set("size", new String[]{"90", "130", "70"});
    model.geom("geom1").run("blk1");
    model.geom("geom1").feature().move("blk1", 0);
    model.geom("geom1").run("imp1");
    model.geom("geom1").run("rot1");
    model.geom("geom1").run("sph1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").run("fin");
    model.geom("geom1").run("mov1");
    model.geom("geom1").create("mov2", "Move");
    model.geom("geom1").feature("mov2").selection("input").set(new String[]{"blk1"});
    model.geom("geom1").feature("mov2").set("displx", "10");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("displx", "-10");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("displx", "-20");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("displx", "-30");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("disply", "-30");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("displz", "-30");
    model.geom("geom1").run("mov2");
    model.geom("geom1").run("mov2");
    model.geom("geom1").create("dif1", "Difference");
    model.geom("geom1").feature("dif1").selection("input").set(new String[]{"mov2"});
    model.geom("geom1").feature("dif1").selection("input2").set(new String[]{"rot1"});
    model.geom("geom1").run("dif1");
    model.geom("geom1").runPre("dif1");
    model.geom("geom1").feature("dif1").selection("input").set(new String[]{});
    model.geom("geom1").feature("dif1").selection("input2").remove(new String[]{"rot1"});
    model.geom("geom1").feature("dif1").selection("input").set(new String[]{"rot1"});
    model.geom("geom1").feature("dif1").selection("input2").set(new String[]{"mov2"});
    model.geom("geom1").run("dif1");
    model.geom("geom1").runPre("dif1");
    model.geom("geom1").feature("dif1").selection("input").set(new String[]{"mov2"});
    model.geom("geom1").feature("dif1").selection("input2").set(new String[]{"rot1"});
    model.geom("geom1").run("dif1");
    model.geom("geom1").runPre("dif1");
    model.geom("geom1").run("dif1");
    model.geom("geom1").run();

    model.mesh("mesh1").autoMeshSize(9);
    model.mesh("mesh1").run();
    model.mesh("mesh1").autoMeshSize(8);
    model.mesh("mesh1").autoMeshSize(7);
    model.mesh("mesh1").run();

    model.geom("geom1").feature().remove("blk1");
    model.geom("geom1").feature().remove("mov2");
    model.geom("geom1").feature().remove("dif1");
    model.geom("geom1").run("imp1");
    model.geom("geom1").run("rot1");
    model.geom("geom1").run("sph1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").create("blk1", "Block");
    model.geom("geom1").feature().remove("blk1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature().create("ext1", "Extrude");
    model.geom("geom1").feature("ext1").set("extrudefrom", "faces");
    model.geom("geom1").feature("ext1").selection("inputface").add("rot1", new int[]{7});
    model.geom("geom1").run("ext1");
    model.geom("geom1").runPre("ext1");
    model.geom("geom1").feature("ext1").setIndex("distance", "14", 0);
    model.geom("geom1").run("ext1");
    model.geom("geom1").feature("ext1").setIndex("distance", "7", 0);
    model.geom("geom1").run("ext1");
    model.geom("geom1").feature("ext1").setIndex("distance", "14", 0);
    model.geom("geom1").run("ext1");
    model.geom("geom1").run("ext1");
    model.geom("geom1").run();

    model.material("mat2").selection().set(new int[]{2});
    model.material("mat1").selection().geom("geom1", 3);
    model.material("mat1").selection().set(new int[]{1});
    model.material("mat3").selection().geom("geom1", 3);
    model.material("mat3").selection().set(new int[]{3});

    model.physics("ht").feature("fluid1").selection().set(new int[]{2});
    model.physics("ht").feature("hf1").selection().set(new int[]{});
    model.physics("ht").feature("hs1").selection().set(new int[]{3});
    model.physics("ht").feature("hf1").selection().all();

    model.material("mat2").selection().all();
    model.material("mat2").selection().set(new int[]{2});

    model.physics().move("spf", 0);
    model.physics("spf").feature().create("iw1", "InteriorWall", 2);
    model.physics("spf").feature("iw1").selection().set(new int[]{6, 7, 8, 9, 10, 19});

    model.label("Untitled2.mph");

    model.material().remove("mat2");
    model.material().remove("mat1");
    model.material().remove("mat3");

    model.geom("geom1").feature().remove("ext1");
    model.geom("geom1").run("imp1");
    model.geom("geom1").run("rot1");
    model.geom("geom1").run("sph1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature().create("ext1", "Extrude");
    model.geom("geom1").feature("ext1").set("extrudefrom", "faces");
    model.geom("geom1").feature("ext1").selection("inputface").add("rot1", new int[]{2});
    model.geom("geom1").feature("ext1").setIndex("distance", "16", 0);
    model.geom("geom1").run("ext1");
    model.geom("geom1").feature("ext1").set("reverse", "on");
    model.geom("geom1").run("ext1");
    model.geom("geom1").run("fin");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature("ext1").set("unite", "off");
    model.geom("geom1").run("ext1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature("ext1").set("crossfaces", "off");
    model.geom("geom1").run("ext1");
    model.geom("geom1").feature().remove("ext1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").feature().create("wp1", "WorkPlane");
    model.geom("geom1").feature("wp1").set("unite", true);
    model.geom("geom1").feature("wp1").set("planetype", "faceparallel");
    model.geom("geom1").feature("wp1").selection("face").set("rot1", 4);

    model.view().create("view3", "geom1", "wp1");

    model.geom("geom1").feature("wp1").set("workplane3d", true);
    model.geom("geom1").feature("wp1").geom().run("");
    model.geom("geom1").feature("wp1").geom().feature().create("r1", "Rectangle");
    model.geom("geom1").feature("wp1").geom().feature("r1").set("type", "solid");
    model.geom("geom1").feature("wp1").geom().feature("r1").set("base", "corner");
    model.geom("geom1").feature("wp1").geom().feature("r1").set("pos", new String[]{"-9", "-17.500000224785"});
    model.geom("geom1").feature("wp1").geom().feature("r1").set("size", new String[]{"0", "0"});
    model.geom("geom1").feature("wp1").geom().run("");
    model.geom("geom1").feature("wp1").geom().feature().remove("r1");
    model.geom("geom1").feature().remove("wp1");
    model.geom("geom1").run("mov1");
    model.geom("geom1").create("blk1", "Block");
    model.geom("geom1").feature("blk1").set("size", new String[]{"100", "100", "100"});
    model.geom("geom1").run("blk1");
    model.geom("geom1").run("blk1");
    model.geom("geom1").create("mov2", "Move");
    model.geom("geom1").feature("mov2").selection("input").set(new String[]{"blk1"});
    model.geom("geom1").feature("mov2").set("displx", "30");
    model.geom("geom1").run("mov2");
    model.geom("geom1").feature("mov2").set("displx", "-30");
    model.geom("geom1").feature("mov2").set("disply", "-30");
    model.geom("geom1").feature("mov2").set("displz", "-30");
    model.geom("geom1").run("mov2");
    model.geom("geom1").run("fin");

    model.material().create("mat1", "Common", "comp1");
    model.material("mat1").label("Air");
    model.material("mat1").set("family", "air");
    model.material("mat1").propertyGroup("def").set("relpermeability", "1");
    model.material("mat1").propertyGroup("def").set("relpermittivity", "1");
    model.material("mat1").propertyGroup("def").set("dynamicviscosity", "eta(T[1/K])[Pa*s]");
    model.material("mat1").propertyGroup("def").set("ratioofspecificheat", "1.4");
    model.material("mat1").propertyGroup("def").set("electricconductivity", "0[S/m]");
    model.material("mat1").propertyGroup("def").set("heatcapacity", "Cp(T[1/K])[J/(kg*K)]");
    model.material("mat1").propertyGroup("def").set("density", "rho(pA[1/Pa],T[1/K])[kg/m^3]");
    model.material("mat1").propertyGroup("def").set("thermalconductivity", "k(T[1/K])[W/(m*K)]");
    model.material("mat1").propertyGroup("def").set("soundspeed", "cs(T[1/K])[m/s]");
    model.material("mat1").propertyGroup("def").func().create("eta", "Piecewise");
    model.material("mat1").propertyGroup("def").func("eta").set("funcname", "eta");
    model.material("mat1").propertyGroup("def").func("eta").set("arg", "T");
    model.material("mat1").propertyGroup("def").func("eta").set("extrap", "constant");
    model.material("mat1").propertyGroup("def").func("eta")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-8.38278E-7+8.35717342E-8*T^1-7.69429583E-11*T^2+4.6437266E-14*T^3-1.06585607E-17*T^4"}});
    model.material("mat1").propertyGroup("def").func().create("Cp", "Piecewise");
    model.material("mat1").propertyGroup("def").func("Cp").set("funcname", "Cp");
    model.material("mat1").propertyGroup("def").func("Cp").set("arg", "T");
    model.material("mat1").propertyGroup("def").func("Cp").set("extrap", "constant");
    model.material("mat1").propertyGroup("def").func("Cp")
         .set("pieces", new String[][]{{"200.0", "1600.0", "1047.63657-0.372589265*T^1+9.45304214E-4*T^2-6.02409443E-7*T^3+1.2858961E-10*T^4"}});
    model.material("mat1").propertyGroup("def").func().create("rho", "Analytic");
    model.material("mat1").propertyGroup("def").func("rho").set("funcname", "rho");
    model.material("mat1").propertyGroup("def").func("rho").set("args", new String[]{"pA", "T"});
    model.material("mat1").propertyGroup("def").func("rho").set("expr", "pA*0.02897/8.314/T");
    model.material("mat1").propertyGroup("def").func("rho").set("dermethod", "manual");
    model.material("mat1").propertyGroup("def").func("rho")
         .set("argders", new String[][]{{"pA", "d(pA*0.02897/8.314/T,pA)"}, {"T", "d(pA*0.02897/8.314/T,T)"}});
    model.material("mat1").propertyGroup("def").func().create("k", "Piecewise");
    model.material("mat1").propertyGroup("def").func("k").set("funcname", "k");
    model.material("mat1").propertyGroup("def").func("k").set("arg", "T");
    model.material("mat1").propertyGroup("def").func("k").set("extrap", "constant");
    model.material("mat1").propertyGroup("def").func("k")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-0.00227583562+1.15480022E-4*T^1-7.90252856E-8*T^2+4.11702505E-11*T^3-7.43864331E-15*T^4"}});
    model.material("mat1").propertyGroup("def").func().create("cs", "Analytic");
    model.material("mat1").propertyGroup("def").func("cs").set("funcname", "cs");
    model.material("mat1").propertyGroup("def").func("cs").set("args", new String[]{"T"});
    model.material("mat1").propertyGroup("def").func("cs").set("expr", "sqrt(1.4*287*T)");
    model.material("mat1").propertyGroup("def").func("cs").set("dermethod", "manual");
    model.material("mat1").propertyGroup("def").func("cs")
         .set("argders", new String[][]{{"T", "d(sqrt(1.4*287*T),T)"}});
    model.material("mat1").propertyGroup("def").addInput("temperature");
    model.material("mat1").propertyGroup("def").addInput("pressure");
    model.material("mat1").propertyGroup().create("RefractiveIndex", "\u6298\u5c04\u7387");
    model.material("mat1").propertyGroup("RefractiveIndex").set("n", "1");
    model.material("mat1").set("family", "air");
    model.material().create("mat2", "Common", "comp1");
    model.material("mat2").label("Concrete");
    model.material("mat2").set("family", "concrete");
    model.material("mat2").propertyGroup("def").set("thermalexpansioncoefficient", "10e-6[1/K]");
    model.material("mat2").propertyGroup("def").set("density", "2300[kg/m^3]");
    model.material("mat2").propertyGroup("def").set("thermalconductivity", "1.8[W/(m*K)]");
    model.material("mat2").propertyGroup("def").set("heatcapacity", "880[J/(kg*K)]");
    model.material("mat2").propertyGroup().create("Enu", "\u6768\u6c0f\u6a21\u91cf\u548c\u6cca\u677e\u6bd4");
    model.material("mat2").propertyGroup("Enu").set("poissonsratio", "0.33");
    model.material("mat2").propertyGroup("Enu").set("youngsmodulus", "25e9[Pa]");
    model.material("mat2").set("family", "concrete");
    model.material("mat2").selection().set(new int[]{2});
    model.material().move("mat2", 0);
    model.material().create("mat3", "Common", "comp1");
    model.material("mat3").label("Iron");
    model.material("mat3").set("family", "iron");
    model.material("mat3").propertyGroup("def").set("relpermeability", "4000");
    model.material("mat3").propertyGroup("def").set("electricconductivity", "1.12e7[S/m]");
    model.material("mat3").propertyGroup("def").set("thermalexpansioncoefficient", "12.2e-6[1/K]");
    model.material("mat3").propertyGroup("def").set("heatcapacity", "440[J/(kg*K)]");
    model.material("mat3").propertyGroup("def").set("relpermittivity", "1");
    model.material("mat3").propertyGroup("def").set("density", "7870[kg/m^3]");
    model.material("mat3").propertyGroup("def").set("thermalconductivity", "76.2[W/(m*K)]");
    model.material("mat3").propertyGroup().create("Enu", "\u6768\u6c0f\u6a21\u91cf\u548c\u6cca\u677e\u6bd4");
    model.material("mat3").propertyGroup("Enu").set("poissonsratio", "0.29");
    model.material("mat3").propertyGroup("Enu").set("youngsmodulus", "200e9[Pa]");
    model.material("mat3").set("family", "iron");
    model.material("mat3").selection().set(new int[]{4});
    model.material().move("mat3", 0);
    model.material().move("mat3", 1);
    model.material("mat1").selection().set(new int[]{1, 2, 3, 4});

    model.physics("ht").feature("hs1").selection().set(new int[]{4});
    model.physics("ht").feature("hf1").selection().set(new int[]{});
    model.physics("ht").feature().remove("hf1");
    model.physics("spf").feature().remove("iw1");
    model.physics("ht").feature("fluid1").selection().all();
    model.physics("ht").feature("fluid1").selection().set(new int[]{3});

    model.mesh("mesh1").automatic(false);
    model.mesh("mesh1").automatic(true);

    model.physics("ht").selection().set(new int[]{2, 3, 4});
    model.physics("spf").selection().set(new int[]{2, 3, 4});

    model.material().move("mat2", 2);
    model.material().move("mat3", 1);

    model.mesh("mesh1").run();
    model.mesh("mesh1").autoMeshSize(5);
    model.mesh("mesh1").run();

    model.view("view1").hideEntities().create("hide1");
    model.view("view1").hideEntities("hide1").geom(3);
    model.view("view1").hideEntities("hide1").add(new int[]{1});
    model.view("view1").hideEntities("hide1").add(new int[]{1});
    model.view("view1").hideEntities("hide1").add(new int[]{1});
    model.view("view1").hideObjects().create("hide1");
    model.view("view1").hideObjects("hide1").init(3);
    model.view("view1").hideObjects("hide1").add("fin", new int[]{1});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("spf").selection().set(new int[]{3});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");
    model.sol("sol2").runAll();

    model.result("pg1").run();

    model.study("std1").feature("time").set("plotgroup", "pg3");

    model.multiphysics().create("tc1", "TemperatureCoupling", "geom1", -1);
    model.multiphysics().create("fc1", "FlowCoupling", "geom1", -1);

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg3");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");
    model.sol("sol2").runAll();

    model.result("pg1").run();
    model.result("pg2").run();
    model.result("pg3").run();
    model.result("pg3").run();
    model.result("pg3").run();
    model.result("pg3").setIndex("looplevel", "72", 0);
    model.result("pg3").setIndex("looplevel", "80", 0);
    model.result("pg4").run();
    model.result("pg4").run();
    model.result("pg4").run();
    model.result("pg4").setIndex("looplevel", "2", 0);
    model.result("pg4").setIndex("looplevel", "11", 0);
    model.result("pg4").setIndex("looplevel", "72", 0);
    model.result("pg4").setIndex("looplevel", "101", 0);
    model.result("pg3").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", "10", 0);
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").setIndex("looplevel", "3", 0);
    model.result("pg1").setIndex("looplevel", "13", 0);
    model.result("pg1").setIndex("looplevel", "71", 0);

    model.multiphysics().remove("tc1");
    model.multiphysics().remove("fc1");

    model.result("pg2").run();
    model.result("pg1").run();
    model.result("pg1").run();

    model.physics("ht").feature().move("fluid1", 3);
    model.physics("ht").feature("hs1").set("heatSourceType", "GeneralSource");
    model.physics("ht").feature("hs1").set("Q", "250");
    model.physics("ht").feature().create("tc1", "ThermalContact", 2);
    model.physics("ht").feature().remove("tc1");
    model.physics("ht").feature().create("hf1", "HeatFluxBoundary", 2);
    model.physics("ht").feature("hf1").selection().all();

    model.view("view1").hideEntities().create("hide2");
    model.view("view1").hideEntities("hide2").geom(2);
    model.view("view1").hideEntities("hide2").add(new int[]{6});
    model.view("view1").hideEntities("hide2").add(new int[]{6});
    model.view("view1").set("geomhidestatus", "ignore");
    model.view("view1").hideEntities("hide1").add(new int[]{1});
    model.view("view1").hideEntities("hide1").add(new int[]{1});

    model.physics("ht").feature("hf1").set("HeatFluxType", "GeneralInwardHeatFlux");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg3");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.study("std1").feature("time").set("plotgroup", "pg4");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");

    return model;
  }

  public static Model run3(Model model) {
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics().move("spf", 1);
    model.physics("spf").feature().create("vf1", "VolumeForce", 3);
    model.physics("spf").feature().remove("vf1");

    model.multiphysics().create("fc1", "FlowCoupling", "geom1", -1);
    model.multiphysics().remove("fc1");
    model.multiphysics().create("tc1", "TemperatureCoupling", "geom1", -1);

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.view("view1").set("geomhidestatus", "hide");

    model.physics("ht").feature("hs1").set("Q", "25000");
    model.physics("ht").feature("hf1").set("HeatFluxType", "GeneralInwardHeatFlux");
    model.physics("ht").feature().remove("hf1");
    model.physics("ht").feature().create("bhs1", "BoundaryHeatSource", 2);

    model.view("view1").hideEntities("hide2").add(new int[]{17});
    model.view("view1").hideEntities("hide2").add(new int[]{19});

    model.physics("ht").feature().remove("bhs1");
    model.physics("ht").feature().create("ds1", "DiffuseSurface", 2);

    model.view("view1").hideEntities("hide2").add(new int[]{21});
    model.view("view1").hideEntities("hide2").add(new int[]{21});

    model.physics("ht").feature("ds1").selection().set(new int[]{18, 20, 22, 23});

    model.view("view1").set("geomhidestatus", "showonlyhidden");
    model.view("view1").hideEntities("hide2").remove(new int[]{19});
    model.view("view1").hideEntities("hide2").remove(new int[]{17});
    model.view("view1").hideEntities("hide2").remove(new int[]{17});
    model.view("view1").hideEntities("hide2").remove(new int[]{21});
    model.view("view1").set("geomhidestatus", "hide");

    model.physics("ht").feature("ds1").selection().set(new int[]{16, 17, 18, 20, 21, 22, 23, 24});
    model.physics("spf").feature().create("vf1", "VolumeForce", 3);
    model.physics("spf").feature().remove("vf1");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").feature("aDef").set("blocksize", 100);
    model.sol("sol2").feature("t1").feature("aDef").set("blocksizeactive", true);
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("ht").feature("ds1").set("epsilon_rad_mat", "from_mat");
    model.physics("ht").feature().remove("ds1");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("spf").feature("init1").set("u", new String[]{"10", "0", "0"});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");
    model.sol("sol2").runAll();

    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickxnumber", "10");
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickplane", "xy");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickznumber", "10");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickznumber", "20");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickplane", "yz");
    model.result("pg1").feature("slc1").set("quickxnumber", "20");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickplane", "zx");
    model.result("pg1").feature("slc1").set("quickynumber", "20");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("rangecoloractive", "on");
    model.result("pg1").feature("slc1").set("rangecolormax", "10.0073192933491");
    model.result("pg1").feature("slc1").set("rangecolormin", "0");
    model.result("pg1").feature("slc1").set("rangecoloractive", "off");
    model.result("pg1").feature("slc1").set("rangedataactive", "on");
    model.result("pg1").feature("slc1").set("rangedatamax", "10.0073192933491");
    model.result("pg1").feature("slc1").set("rangedatamin", "0");
    model.result("pg1").feature("slc1").set("rangedatamax", "10.0073192933491");
    model.result("pg1").feature("slc1").set("rangedataactive", "off");
    model.result("pg1").feature("slc1").set("quickplane", "xy");
    model.result("pg1").feature("slc1").set("quickznumber", "20");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("interactive", "on");
    model.result("pg1").feature("slc1").set("shift", "-2");
    model.result("pg1").feature("slc1").set("interactive", "off");
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg3").run();
    model.result("pg4").run();
    model.result("pg4").run();
    model.result("pg1").run();
    model.result("pg3").run();
    model.result("pg3").run();
    model.result("pg3").setIndex("looplevel", "11", 0);
    model.result("pg3").setIndex("looplevel", "72", 0);
    model.result("pg3").setIndex("looplevel", "101", 0);
    model.result("pg3").setIndex("looplevel", "89", 0);

    model.physics("spf").feature("init1").set("u", new String[]{"0", "0", "0"});
    model.physics("spf").feature().create("ifan1", "InteriorFan", 2);
    model.physics("spf").feature("ifan1").selection().all();
    model.physics().move("spf", 0);
    model.physics("spf").feature().remove("ifan1");
    model.physics("spf").feature().create("fan1", "ExtFan", 2);
    model.physics("spf").feature("fan1").selection().set(new int[]{15});
    model.physics("spf").feature("fan1").set("pinput", "10");
    model.physics("spf").feature().create("fan2", "ExtFan", 2);
    model.physics("spf").feature("fan2").selection().set(new int[]{12});
    model.physics("spf").feature("fan2").set("FlowDirection", "Outlet");
    model.physics("spf").feature("fan2").set("pexit", "-10");
    model.physics().move("spf", 1);

    model.mesh("mesh1").current("ftet2");

    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("t1");

    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").current("ftet2");
    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").autoMeshSize(4);
    model.mesh("mesh1").clearMesh();
    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").autoMeshSize(5);
    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").current("ftet2");
    model.mesh("mesh1").current("ftet2");

    model.physics().move("spf", 0);

    model.mesh("mesh1").current("ftet2");

    model.physics("spf").feature().remove("fan1");
    model.physics("spf").feature().remove("fan2");
    model.physics("spf").feature("init1").set("u", new String[]{"0", "50", "0"});

    model.label("Untitled2.mph");

    model.physics("spf").feature().create("prpc1", "PressurePointConstraint", 0);
    model.physics("spf").feature("prpc1").selection().all();
    model.physics("spf").feature("init1").set("u", new String[]{"0", "0", "0"});

    model.label("Untitled2.mph");

    model.mesh("mesh1").current("ftet2");

    model.physics("spf").feature().remove("prpc1");

    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").run();

    model.physics("spf").feature().create("prpc1", "PressurePointConstraint", 0);
    model.physics("spf").feature("prpc1").selection().all();
    model.physics("spf").feature("prpc1").selection().set(new int[]{9, 10, 11, 12, 19, 20, 21, 22});

    model.mesh("mesh1").run();
    model.mesh("mesh1").run();

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("spf").feature().create("vf1", "VolumeForce", 3);
    model.physics("spf").feature("vf1").selection().set(new int[]{3});
    model.physics("spf").feature("vf1").set("F", new String[]{"0", "0", "10"});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg4");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("fc1", "FullyCoupled");
    model.sol("sol2").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol2").feature("t1").feature("fc1").set("maxiter", 6);
    model.sol("sol2").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("fc1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol2").feature("t1").feature("fc1").set("maxiter", 6);
    model.sol("sol2").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("spf").feature().remove("vf1");

    model.multiphysics("nitf1").set("SpecifyDensity", "FromHeatTransferInterface");
    model.multiphysics().remove("tc1");

    model.physics("spf").feature().create("out1", "OutletBoundary", 2);
    model.physics("spf").feature("out1").selection().set(new int[]{13, 14});

    model.mesh("mesh1").current("ftet2");

    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("t1");

    model.geom("geom1").feature().remove("imp1");
    model.geom("geom1").feature().remove("rot1");
    model.geom("geom1").feature().remove("sph1");
    model.geom("geom1").feature().remove("mov1");
    model.geom("geom1").feature().remove("blk1");
    model.geom("geom1").feature().remove("mov2");
    model.geom("geom1").runPre("fin");
    model.geom("geom1").runPre("fin");
    model.geom("geom1").run("fin");
    model.geom("geom1").run("fin");
    model.geom("geom1").runPre("fin");
    model.geom("geom1").create("blk1", "Block");
    model.geom("geom1").feature("blk1").set("size", new String[]{"30", "20", "10"});
    model.geom("geom1").run("blk1");
    model.geom("geom1").run("blk1");
    model.geom("geom1").create("sph1", "Sphere");
    model.geom("geom1").run("sph1");
    model.geom("geom1").feature("sph1").set("pos", new String[]{"10", "0", "0"});
    model.geom("geom1").run("sph1");
    model.geom("geom1").feature("sph1").set("pos", new String[]{"15", "10", "5"});
    model.geom("geom1").run("sph1");
    model.geom("geom1").run("fin");

    model.material().remove("mat2");
    model.material("mat1").selection().set(new int[]{1});
    model.material("mat3").selection().set(new int[]{2});

    model.geom("geom1").runPre("fin");

    model.view("view1").set("geomhidestatus", "ignore");

    model.mesh("mesh1").run();
    model.mesh("mesh1").automatic(true);
    model.mesh("mesh1").run();

    model.material("mat1").selection().all();
    model.material("mat1").selection().set(new int[]{1});

    model.geom("geom1").runPre("fin");

    model.physics("spf").feature("prpc1").selection().all();
    model.physics("spf").feature().remove("prpc1");
    model.physics("spf").feature().remove("out1");
    model.physics("ht").feature("fluid1").selection().all();
    model.physics("ht").feature("fluid1").selection().set(new int[]{});
    model.physics("spf").selection().set(new int[]{1});
    model.physics("ht").selection().set(new int[]{1, 2});
    model.physics("spf").feature().create("inl1", "InletBoundary", 2);
    model.physics("spf").feature("inl1").selection().set(new int[]{1});
    model.physics("spf").feature().create("out1", "OutletBoundary", 2);
    model.physics("spf").feature("out1").selection().set(new int[]{14});
    model.physics("ht").feature("fluid1").selection().set(new int[]{1});
    model.physics("ht").feature("hs1").selection().set(new int[]{2});

    model.mesh("mesh1").run();

    model.study("std1").feature("time").set("plotgroup", "pg1");

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("i1", "Iterative");
    model.sol("sol2").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol2").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol2").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol2").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol2").feature("t1").feature("i1").set("maxlinit", 50);
    model.sol("sol2").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol2").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("prefun", "gmg");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("mcasegen", "any");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").set("gmglevels", 1);
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "i1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);

    return model;
  }

  public static Model run4(Model model) {
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.physics("spf").feature().remove("inl1");
    model.physics("spf").feature("out1").selection().set(new int[]{1, 3, 4, 14});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickplane", "yz");
    model.result("pg1").run();
    model.result("pg1").feature("slc1").set("quickplane", "zx");
    model.result("pg1").run();

    model.physics("spf").feature("out1").selection().set(new int[]{3, 4});
    model.physics("spf").feature().create("prpc1", "PressurePointConstraint", 0);
    model.physics("spf").feature("prpc1").selection().all();
    model.physics("spf").feature("prpc1").selection().set(new int[]{1, 2, 3, 4, 11, 12, 13, 14});

    model.sol("sol2").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol2").feature().remove("t1");
    model.sol("sol2").feature().remove("v1");
    model.sol("sol2").feature().remove("st1");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").feature("st1").set("study", "std1");
    model.sol("sol2").feature("st1").set("studystep", "time");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").feature("v1").set("control", "time");
    model.sol("sol2").create("t1", "Time");
    model.sol("sol2").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol2").feature("t1").set("plot", "on");
    model.sol("sol2").feature("t1").set("plotgroup", "pg1");
    model.sol("sol2").feature("t1").set("plotfreq", "tout");
    model.sol("sol2").feature("t1").set("probesel", "all");
    model.sol("sol2").feature("t1").set("probes", new String[]{});
    model.sol("sol2").feature("t1").set("probefreq", "tsteps");
    model.sol("sol2").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol2").feature("t1").set("atolglobal", 5.0E-4);
    model.sol("sol2").feature("t1").set("estrat", "exclude");
    model.sol("sol2").feature("t1").set("maxorder", 2);
    model.sol("sol2").feature("t1").set("control", "time");
    model.sol("sol2").feature("t1").create("seDef", "Segregated");
    model.sol("sol2").feature("t1").create("se1", "Segregated");
    model.sol("sol2").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol2").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol2").feature("t1").create("d1", "Direct");
    model.sol("sol2").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol2").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol2").feature("t1").create("d2", "Direct");
    model.sol("sol2").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol2").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol2").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol2").feature("t1").feature().remove("fcDef");
    model.sol("sol2").feature("t1").feature().remove("seDef");
    model.sol("sol2").attach("std1");

    model.multiphysics("nitf1").setIndex("includeWorkDoneByPressureChanges", "1", 0);
    model.multiphysics("nitf1").setIndex("includeWorkDoneByPressureChanges", "0", 0);
    model.multiphysics("nitf1").setIndex("includeViscousDissipation", "1", 0);
    model.multiphysics("nitf1").setIndex("includeViscousDissipation", "0", 0);
    model.multiphysics("nitf1").set("ThermalTurbType", "KaysCrawford");
    model.multiphysics().create("fc1", "FlowCoupling", "geom1", -1);
    model.multiphysics().remove("fc1");

    model.physics("spf").prop("PhysicalModelProperty").set("TurbulenceModelType", "None");
    model.physics("spf").prop("PhysicalModelProperty").setIndex("StokesFlowProp", "1", 0);
    model.physics("spf").prop("PhysicalModelProperty").setIndex("StokesFlowProp", "0", 0);
    model.physics("spf").prop("PhysicalModelProperty").set("TurbulenceModelType", "RANS");
    model.physics("spf").prop("PhysicalModelProperty").set("TurbulenceModel", "AlgebraicYplus");
    model.physics("spf").prop("PhysicalModelProperty").set("TurbulenceModelType", "None");
    model.physics("ht").prop("PhysicalModelProperty").setIndex("RadiationInParticipatingMedia", "1", 0);
    model.physics("ht").prop("PhysicalModelProperty").setIndex("SurfaceToSurfaceRadiation", "1", 0);
    model.physics("ht").prop("PhysicalModelProperty").setIndex("SurfaceToSurfaceRadiation", "0", 0);
    model.physics("ht").prop("PhysicalModelProperty").setIndex("RadiationInParticipatingMedia", "0", 0);

    model.mesh("mesh1").autoMeshSize(6);
    model.mesh("mesh1").run();

    model.physics("spf").feature().create("vf1", "VolumeForce", 3);
    model.physics("spf").feature("vf1").set("F", new String[]{"0", "0", "mat1.rho*9.8"});
    model.physics("spf").feature("vf1").selection().set(new int[]{1});
    model.physics("spf").feature("vf1").set("F", new String[]{"0", "0", "comp1.mat1.rho*9.8"});

    model.label("Untitled2.mph");

    model.physics("spf").feature("vf1").set("F", new String[]{"0", "0", "-nitf1.rho*g_const"});
    model.physics("spf").feature("out1").selection().set(new int[]{4});

    model.study("std1").feature("time").set("tlist", "range(0,1,100)");

    model.physics("spf").feature().remove("prpc1");

    model.geom("geom1").feature("sph1").set("pos", new String[]{"15", "10", "2"});
    model.geom("geom1").runPre("fin");
    model.geom("geom1").run("fin");

    model.physics("ht").feature().move("fluid1", 7);
    model.physics().move("ht", 0);

    model.study("std1").feature("time").set("plotgroup", "pg4");

    model.mesh("mesh1").autoMeshSize(7);
    model.mesh("mesh1").run();
    model.mesh("mesh1").autoMeshSize(8);
    model.mesh("mesh1").run();

    model.geom("geom1").run("sph1");
    model.geom("geom1").create("dif1", "Difference");
    model.geom("geom1").feature("dif1").selection("input").set(new String[]{"blk1"});
    model.geom("geom1").feature("dif1").selection("input2").set(new String[]{"sph1"});
    model.geom("geom1").run("dif1");
    model.geom("geom1").runPre("fin");
    model.geom("geom1").run("fin");
    model.geom("geom1").runPre("fin");

    model.material("mat1").selection().set(new int[]{1});

    model.geom("geom1").run("fin");

    model.material("mat1").selection().all();

    model.geom("geom1").feature("dif1").set("keep", "on");
    model.geom("geom1").run("dif1");
    model.geom("geom1").feature("dif1").set("createselection", "off");
    model.geom("geom1").run();

    model.material("mat3").selection().all();
    model.material("mat1").selection().set(new int[]{});
    model.material("mat3").selection().set(new int[]{2});
    model.material("mat1").selection().set(new int[]{1});

    model.geom("geom1").feature().remove("dif1");
    model.geom("geom1").run("fin");

    model.material("mat1").selection().all();

    model.mesh("mesh1").autoMeshSize(9);
    model.mesh("mesh1").run();

    model.physics("ht").selection().set(new int[]{1, 2});
    model.physics("ht").feature("hs1").selection().set(new int[]{2});
    model.physics("spf").selection().set(new int[]{1, 2});
    model.physics("ht").feature("fluid1").selection().set(new int[]{1, 2});

    model.material().remove("mat3");

    model.geom("geom1").feature().remove("sph1");
    model.geom("geom1").runPre("fin");
    model.geom("geom1").run();

    model.physics("ht").feature().remove("hs1");

    model.geom("geom1").runPre("fin");

    model.physics("ht").feature().create("bhs1", "BoundaryHeatSource", 2);
    model.physics("ht").feature("bhs1").selection().set(new int[]{3});
    model.physics("ht").feature("bhs1").set("Qb", "25000");

    model.mesh("mesh1").run();

    model.study("std1").feature("time").set("useadvanceddisable", "off");

    model.physics().move("ht", 1);
    model.physics("spf").feature().remove("out1");

    model.study("std1").feature("time").set("plotgroup", "pg1");

    model.multiphysics("nitf1").set("SpecifyDensity", "FromHeatTransferInterface");

    model.physics("ht").feature("bhs1").selection().set(new int[]{1});
    model.physics("ht").feature().create("bhs2", "BoundaryHeatSource", 2);
    model.physics("ht").feature("bhs2").selection().set(new int[]{6});
    model.physics("ht").feature("bhs2").set("Qb", "-25000");
    model.physics("ht").feature("bhs2").set("heatSourceType", "GeneralSource");

    model.study("std1").feature("time").set("plotgroup", "pg4");

    model.sol("sol2").runAll();

    model.result("pg1").run();

    model.label("Untitled2.mph");

    model.result("pg1").run();
    model.result().export().create("anim1", "Animation");
    model.result().export("anim1").set("height", "480");
    model.result().export("anim1").set("width", "640");
    model.result().export("anim1").set("lockratio", "off");
    model.result().export("anim1").set("resolution", "96");
    model.result().export("anim1").set("size", "manual");
    model.result().export("anim1").set("antialias", "off");
    model.result().export("anim1").set("title", "on");
    model.result().export("anim1").set("legend", "on");
    model.result().export("anim1").set("logo", "on");
    model.result().export("anim1").set("options", "off");
    model.result().export("anim1").set("fontsize", "9");
    model.result().export("anim1").set("customcolor", new double[]{1, 1, 1});
    model.result().export("anim1").set("background", "current");
    model.result().export("anim1").set("axisorientation", "on");
    model.result().export("anim1").set("grid", "on");
    model.result().export("anim1").set("axes", "on");
    model.result("pg1").set("window", "graphics");
    model.result("pg1").run();
    model.result("pg1").set("window", "graphics");
    model.result("pg1").set("windowtitle", "");
    model.result().export("anim1").set("giffilename", "C:\\Users\\16413\\Desktop\\FFCS\\TEMP\\Untitled.gif");
    model.result().export("anim1").set("looplevelinput", "interp");
    model.result().export("anim1").set("interp", "range(1,0.1,100)");
    model.result().export("anim1").set("framesel", "all");
    model.result().export("anim1").set("size", "current");
    model.result().export("anim1").run();
    model.result().export("anim1").set("looplevelinput", "all");
    model.result().export("anim1").run();
    model.result().export("anim1").run();
    model.result().export("anim1").set("plotgroup", "pg3");
    model.result().export("anim1").set("looplevelinput", "manualindices");
    model.result().export("anim1").set("looplevelindices", "1-11");
    model.result().export("anim1").set("giffilename", "C:\\Users\\16413\\Desktop\\FFCS\\TEMP\\Untitled2.gif");
    model.result().export("anim1").set("looplevelinput", "manual");
    model.result().export("anim1")
         .set("looplevel", new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
         "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
         "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", 
         "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", 
         "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", 
         "51"});
    model.result().export("anim1").run();
    model.result().export("anim1").set("plotgroup", "pg4");
    model.result().export("anim1").set("giffilename", "C:\\Users\\16413\\Desktop\\FFCS\\TEMP\\Untitled3.gif");
    model.result().export("anim1").run();
    model.result().export("anim1").set("plotgroup", "pg1");
    model.result().export("anim1").set("giffilename", "C:\\Users\\16413\\Desktop\\FFCS\\TEMP\\Untitled.gif");
    model.result().export("anim1").run();
    model.result().export("anim1").set("plotgroup", "pg2");
    model.result().export("anim1").set("giffilename", "C:\\Users\\16413\\Desktop\\FFCS\\TEMP\\Untitled4.gif");
    model.result().export("anim1").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg1").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").set("edges", "on");
    model.result("pg2").setIndex("looplevel", "6", 0);
    model.result("pg2").setIndex("looplevel", "59", 0);
    model.result("pg2").setIndex("looplevel", "90", 0);
    model.result("pg2").setIndex("looplevel", "1", 0);

    model.multiphysics().create("tc1", "TemperatureCoupling", "geom1", -1);
    model.multiphysics().remove("tc1");

    model.label("Untitled2.mph");

    model.geom("geom1").geomRep("comsol");
    model.geom("geom1").run("blk1");
    model.geom("geom1").run("fin");
    model.geom("geom1").runPre("fin");

    return model;
  }

  public static void main(String[] args) {
    Model model = run();
    model = run2(model);
    model = run3(model);
    run4(model);
  }

}
