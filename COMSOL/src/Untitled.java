/*
 * Untitled.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on Mar 11 2021, 00:04 by COMSOL 5.6.0.280. */
public class Untitled {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model.modelPath("C:\\Users\\16413\\Desktop\\FFCS\\TEMP");

    model.component().create("comp1", true);

    model.component("comp1").geom().create("geom1", 3);

    model.component("comp1").mesh().create("mesh1");

    model.component("comp1").physics().create("ht", "HeatTransferInSolidsAndFluids", "geom1");
    model.component("comp1").physics("ht").prop("ShapeProperty").set("order_temperature", "1");
    model.component("comp1").physics().create("spf", "LaminarFlow", "geom1");
    model.component("comp1").physics("spf").prop("AdvancedSettingProperty").set("UsePseudoTime", "1");
    model.component("comp1").physics("spf").prop("PhysicalModelProperty")
         .set("Compressibility", "WeaklyCompressible");

    model.component("comp1").multiphysics().create("nitf1", "NonIsothermalFlow", 3);
    model.component("comp1").multiphysics("nitf1").set("Fluid_physics", "spf");
    model.component("comp1").multiphysics("nitf1").set("Heat_physics", "ht");

    model.study().create("std1");
    model.study("std1").create("time", "Transient");
    model.study("std1").feature("time").activate("ht", true);
    model.study("std1").feature("time").activate("spf", true);
    model.study("std1").feature("time").activate("nitf1", true);

    model.component("comp1").geom("geom1").create("blk1", "Block");
    model.component("comp1").geom("geom1").feature("blk1").set("size", new int[]{30, 20, 10});
    model.component("comp1").geom("geom1").runPre("fin");
    model.component("comp1").geom("geom1").run();

    model.component("comp1").material().create("mat1", "Common");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("eta", "Piecewise");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("Cp", "Piecewise");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("rho", "Analytic");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("k", "Piecewise");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("cs", "Analytic");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("an1", "Analytic");
    model.component("comp1").material("mat1").propertyGroup("def").func().create("an2", "Analytic");
    model.component("comp1").material("mat1").propertyGroup().create("RefractiveIndex", "Refractive index");
    model.component("comp1").material("mat1").propertyGroup().create("NonlinearModel", "Nonlinear model");
    model.component("comp1").material("mat1").propertyGroup().create("idealGas", "Ideal gas");
    model.component("comp1").material("mat1").propertyGroup("idealGas").func().create("Cp", "Piecewise");
    model.component("comp1").material("mat1").label("Air");
    model.component("comp1").material("mat1").set("family", "air");
    model.component("comp1").material("mat1").propertyGroup("def").label("Basic");
    model.component("comp1").material("mat1").propertyGroup("def").func("eta").label("Piecewise");
    model.component("comp1").material("mat1").propertyGroup("def").func("eta").set("arg", "T");
    model.component("comp1").material("mat1").propertyGroup("def").func("eta")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-8.38278E-7+8.35717342E-8*T^1-7.69429583E-11*T^2+4.6437266E-14*T^3-1.06585607E-17*T^4"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("eta").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("def").func("eta").set("fununit", "Pa*s");
    model.component("comp1").material("mat1").propertyGroup("def").func("Cp").label("Piecewise 2");
    model.component("comp1").material("mat1").propertyGroup("def").func("Cp").set("arg", "T");
    model.component("comp1").material("mat1").propertyGroup("def").func("Cp")
         .set("pieces", new String[][]{{"200.0", "1600.0", "1047.63657-0.372589265*T^1+9.45304214E-4*T^2-6.02409443E-7*T^3+1.2858961E-10*T^4"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("Cp").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("def").func("Cp").set("fununit", "J/(kg*K)");
    model.component("comp1").material("mat1").propertyGroup("def").func("rho").label("Analytic");
    model.component("comp1").material("mat1").propertyGroup("def").func("rho")
         .set("expr", "pA*0.02897/R_const[K*mol/J]/T");
    model.component("comp1").material("mat1").propertyGroup("def").func("rho").set("args", new String[]{"pA", "T"});
    model.component("comp1").material("mat1").propertyGroup("def").func("rho").set("argunit", "Pa,K");
    model.component("comp1").material("mat1").propertyGroup("def").func("rho").set("fununit", "kg/m^3");
    model.component("comp1").material("mat1").propertyGroup("def").func("rho")
         .set("plotargs", new String[][]{{"pA", "0", "1"}, {"T", "0", "1"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("k").label("Piecewise 3");
    model.component("comp1").material("mat1").propertyGroup("def").func("k").set("arg", "T");
    model.component("comp1").material("mat1").propertyGroup("def").func("k")
         .set("pieces", new String[][]{{"200.0", "1600.0", "-0.00227583562+1.15480022E-4*T^1-7.90252856E-8*T^2+4.11702505E-11*T^3-7.43864331E-15*T^4"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("k").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("def").func("k").set("fununit", "W/(m*K)");
    model.component("comp1").material("mat1").propertyGroup("def").func("cs").label("Analytic 2");
    model.component("comp1").material("mat1").propertyGroup("def").func("cs")
         .set("expr", "sqrt(1.4*R_const[K*mol/J]/0.02897*T)");
    model.component("comp1").material("mat1").propertyGroup("def").func("cs").set("args", new String[]{"T"});
    model.component("comp1").material("mat1").propertyGroup("def").func("cs").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("def").func("cs").set("fununit", "m/s");
    model.component("comp1").material("mat1").propertyGroup("def").func("cs")
         .set("plotargs", new String[][]{{"T", "273.15", "373.15"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("an1").label("Analytic 1");
    model.component("comp1").material("mat1").propertyGroup("def").func("an1").set("funcname", "alpha_p");
    model.component("comp1").material("mat1").propertyGroup("def").func("an1")
         .set("expr", "-1/rho(pA,T)*d(rho(pA,T),T)");
    model.component("comp1").material("mat1").propertyGroup("def").func("an1").set("args", new String[]{"pA", "T"});
    model.component("comp1").material("mat1").propertyGroup("def").func("an1").set("argunit", "Pa,K");
    model.component("comp1").material("mat1").propertyGroup("def").func("an1").set("fununit", "1/K");
    model.component("comp1").material("mat1").propertyGroup("def").func("an1")
         .set("plotargs", new String[][]{{"pA", "101325", "101325"}, {"T", "273.15", "373.15"}});
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").label("Analytic 2a");
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").set("funcname", "muB");
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").set("expr", "0.6*eta(T)");
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").set("args", new String[]{"T"});
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("def").func("an2").set("fununit", "Pa*s");
    model.component("comp1").material("mat1").propertyGroup("def").func("an2")
         .set("plotargs", new String[][]{{"T", "200", "1600"}});
    model.component("comp1").material("mat1").propertyGroup("def").set("thermalexpansioncoefficient", "");
    model.component("comp1").material("mat1").propertyGroup("def").set("molarmass", "");
    model.component("comp1").material("mat1").propertyGroup("def").set("bulkviscosity", "");
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("thermalexpansioncoefficient", new String[]{"alpha_p(pA,T)", "0", "0", "0", "alpha_p(pA,T)", "0", "0", "0", "alpha_p(pA,T)"});
    model.component("comp1").material("mat1").propertyGroup("def").set("molarmass", "0.02897[kg/mol]");
    model.component("comp1").material("mat1").propertyGroup("def").set("bulkviscosity", "muB(T)");
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("relpermeability", new String[]{"1", "0", "0", "0", "1", "0", "0", "0", "1"});
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("relpermittivity", new String[]{"1", "0", "0", "0", "1", "0", "0", "0", "1"});
    model.component("comp1").material("mat1").propertyGroup("def").set("dynamicviscosity", "eta(T)");
    model.component("comp1").material("mat1").propertyGroup("def").set("ratioofspecificheat", "1.4");
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("electricconductivity", new String[]{"0[S/m]", "0", "0", "0", "0[S/m]", "0", "0", "0", "0[S/m]"});
    model.component("comp1").material("mat1").propertyGroup("def").set("heatcapacity", "Cp(T)");
    model.component("comp1").material("mat1").propertyGroup("def").set("density", "rho(pA,T)");
    model.component("comp1").material("mat1").propertyGroup("def")
         .set("thermalconductivity", new String[]{"k(T)", "0", "0", "0", "k(T)", "0", "0", "0", "k(T)"});
    model.component("comp1").material("mat1").propertyGroup("def").set("soundspeed", "cs(T)");
    model.component("comp1").material("mat1").propertyGroup("def").addInput("temperature");
    model.component("comp1").material("mat1").propertyGroup("def").addInput("pressure");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex").label("Refractive index");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex").set("n", "");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex").set("ki", "");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex").set("n", "");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex").set("ki", "");
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex")
         .set("n", new String[]{"1", "0", "0", "0", "1", "0", "0", "0", "1"});
    model.component("comp1").material("mat1").propertyGroup("RefractiveIndex")
         .set("ki", new String[]{"0", "0", "0", "0", "0", "0", "0", "0", "0"});
    model.component("comp1").material("mat1").propertyGroup("NonlinearModel").label("Nonlinear model");
    model.component("comp1").material("mat1").propertyGroup("NonlinearModel").set("BA", "(def.gamma+1)/2");
    model.component("comp1").material("mat1").propertyGroup("idealGas").label("Ideal gas");
    model.component("comp1").material("mat1").propertyGroup("idealGas").func("Cp").label("Piecewise 2");
    model.component("comp1").material("mat1").propertyGroup("idealGas").func("Cp").set("arg", "T");
    model.component("comp1").material("mat1").propertyGroup("idealGas").func("Cp")
         .set("pieces", new String[][]{{"200.0", "1600.0", "1047.63657-0.372589265*T^1+9.45304214E-4*T^2-6.02409443E-7*T^3+1.2858961E-10*T^4"}});
    model.component("comp1").material("mat1").propertyGroup("idealGas").func("Cp").set("argunit", "K");
    model.component("comp1").material("mat1").propertyGroup("idealGas").func("Cp").set("fununit", "J/(kg*K)");
    model.component("comp1").material("mat1").propertyGroup("idealGas").set("Rs", "R_const/Mn");
    model.component("comp1").material("mat1").propertyGroup("idealGas").set("heatcapacity", "Cp(T)");
    model.component("comp1").material("mat1").propertyGroup("idealGas").set("ratioofspecificheat", "1.4");
    model.component("comp1").material("mat1").propertyGroup("idealGas").set("molarmass", "0.02897");
    model.component("comp1").material("mat1").propertyGroup("idealGas").addInput("temperature");
    model.component("comp1").material("mat1").propertyGroup("idealGas").addInput("pressure");
    model.component("comp1").material("mat1").set("groups", new String[][]{});
    model.component("comp1").material("mat1").set("family", "air");

    model.component("comp1").physics("ht").feature("fluid1").selection().set(1);
    model.component("comp1").physics("ht").create("bhs1", "BoundaryHeatSource", 2);
    model.component("comp1").physics("ht").feature("bhs1").selection().set(1);
    model.component("comp1").physics("ht").feature("bhs1").set("Qb", 2500);
    model.component("comp1").physics("ht").create("bhs2", "BoundaryHeatSource", 2);

    model.component("comp1").view("view1").set("transparency", true);

    model.component("comp1").physics("ht").feature("bhs2").selection().set(6);
    model.component("comp1").physics("ht").feature("bhs2").set("Qb", -2500);
    model.component("comp1").physics("spf").create("vf1", "VolumeForce", 3);
    model.component("comp1").physics("spf").feature("vf1").set("F", new String[]{"0", "0", "-ht.rho*g_const"});
    model.component("comp1").physics("spf").feature("vf1").selection().set(1);
    model.component("comp1").physics("spf").feature("vf1").set("F", new String[]{"0", "0", "-ht.rho*g_const"});

    model.component("comp1").mesh("mesh1").autoMeshSize(7);
    model.component("comp1").mesh("mesh1").run();
    model.component("comp1").mesh("mesh1").autoMeshSize(8);
    model.component("comp1").mesh("mesh1").run();
    model.component("comp1").mesh("mesh1").autoMeshSize(9);
    model.component("comp1").mesh("mesh1").run();
    model.component("comp1").mesh("mesh1").autoMeshSize(8);
    model.component("comp1").mesh("mesh1").run();
    model.component("comp1").mesh("mesh1").autoMeshSize(7);
    model.component("comp1").mesh("mesh1").run();

    model.study("std1").feature("time").set("plot", true);
    model.study("std1").feature("time").set("tlist", "range(0,0.1,10)");

    model.sol().create("sol1");
    model.sol("sol1").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").feature("st1").set("study", "std1");
    model.sol("sol1").feature("st1").set("studystep", "time");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").feature("v1").set("control", "time");
    model.sol("sol1").create("t1", "Time");
    model.sol("sol1").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol1").feature("t1").set("plot", "on");
    model.sol("sol1").feature("t1").set("plotgroup", "Default");
    model.sol("sol1").feature("t1").set("plotfreq", "tout");
    model.sol("sol1").feature("t1").set("probesel", "all");
    model.sol("sol1").feature("t1").set("probes", new String[]{});
    model.sol("sol1").feature("t1").set("probefreq", "tsteps");
    model.sol("sol1").feature("t1").set("rtol", 0.005);
    model.sol("sol1").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol1").feature("t1").set("atolglobalfactor", 0.05);
    model.sol("sol1").feature("t1").set("atolglobalvaluemethod", "factor");
    model.sol("sol1").feature("t1")
         .set("atolmethod", new String[]{"comp1_p", "scaled", "comp1_T", "global", "comp1_u", "global"});
    model.sol("sol1").feature("t1")
         .set("atol", new String[]{"comp1_p", "1e-3", "comp1_T", "1e-3", "comp1_u", "1e-3"});
    model.sol("sol1").feature("t1")
         .set("atolvaluemethod", new String[]{"comp1_p", "factor", "comp1_T", "factor", "comp1_u", "factor"});
    model.sol("sol1").feature("t1")
         .set("atolfactor", new String[]{"comp1_p", "1", "comp1_T", "0.1", "comp1_u", "0.1"});
    model.sol("sol1").feature("t1").set("endtimeinterpolation", true);
    model.sol("sol1").feature("t1").set("estrat", "exclude");
    model.sol("sol1").feature("t1").set("rhoinf", 0.5);
    model.sol("sol1").feature("t1").set("predictor", "constant");
    model.sol("sol1").feature("t1").set("maxorder", 2);
    model.sol("sol1").feature("t1").set("stabcntrl", true);
    model.sol("sol1").feature("t1").set("bwinitstepfrac", "0.01");
    model.sol("sol1").feature("t1").set("control", "time");
    model.sol("sol1").feature("t1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("t1").create("seDef", "Segregated");
    model.sol("sol1").feature("t1").create("se1", "Segregated");
    model.sol("sol1").feature("t1").feature("se1").feature().remove("ssDef");
    model.sol("sol1").feature("t1").feature("se1").create("ss1", "SegregatedStep");
    model.sol("sol1").feature("t1").feature("se1").feature("ss1").set("segvar", new String[]{"comp1_u", "comp1_p"});
    model.sol("sol1").feature("t1").feature("se1").feature("ss1").set("subdamp", 0.8);
    model.sol("sol1").feature("t1").feature("se1").feature("ss1").set("subjtech", "once");
    model.sol("sol1").feature("t1").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d1").set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("d1")
         .label("\u76f4\u63a5\uff0c\u6d41\u4f53\u6d41\u52a8\u53d8\u91cf (spf)");
    model.sol("sol1").feature("t1").feature("se1").feature("ss1").set("linsolver", "d1");
    model.sol("sol1").feature("t1").feature("se1").feature("ss1").label("\u901f\u5ea6 u\uff0c\u538b\u529b p");
    model.sol("sol1").feature("t1").feature("se1").create("ss2", "SegregatedStep");
    model.sol("sol1").feature("t1").feature("se1").feature("ss2").set("segvar", new String[]{"comp1_T"});
    model.sol("sol1").feature("t1").feature("se1").feature("ss2").set("subdamp", 0.8);
    model.sol("sol1").feature("t1").feature("se1").feature("ss2").set("subjtech", "once");
    model.sol("sol1").feature("t1").create("d2", "Direct");
    model.sol("sol1").feature("t1").feature("d2").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d2").set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("d2").label("\u76f4\u63a5\uff0c\u6e29\u5ea6 (ht)");
    model.sol("sol1").feature("t1").feature("se1").feature("ss2").set("linsolver", "d2");
    model.sol("sol1").feature("t1").feature("se1").feature("ss2").label("\u6e29\u5ea6");
    model.sol("sol1").feature("t1").feature("se1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("se1").set("segstabacc", "segaacc");
    model.sol("sol1").feature("t1").feature("se1").set("segaaccdim", 5);
    model.sol("sol1").feature("t1").feature("se1").set("segaaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("se1").set("segaaccdelay", 1);
    model.sol("sol1").feature("t1").feature("se1").set("maxsegiter", 10);
    model.sol("sol1").feature("t1").feature("se1").create("ll1", "LowerLimit");
    model.sol("sol1").feature("t1").feature("se1").feature("ll1").set("lowerlimit", "comp1.T 0");
    model.sol("sol1").feature("t1").create("i1", "Iterative");
    model.sol("sol1").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i1").set("maxlinit", 100);
    model.sol("sol1").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i1").label("AMG\uff0c\u6d41\u4f53\u6d41\u52a8\u53d8\u91cf (spf)");
    model.sol("sol1").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("maxcoarsedof", 80000);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("strconn", 0.02);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("iter", 0);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("iter", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").create("i2", "Iterative");
    model.sol("sol1").feature("t1").feature("i2").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i2").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i2").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i2").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i2").set("maxlinit", 10000);
    model.sol("sol1").feature("t1").feature("i2").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i2").label("AMG\uff0c\u6e29\u5ea6 (ht)");
    model.sol("sol1").feature("t1").feature("i2").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("maxcoarsedof", 50000);
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("strconn", 0.01);
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").feature("pr").create("so1", "SOR");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").feature("po").create("so1", "SOR");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i2").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature().remove("fcDef");
    model.sol("sol1").feature("t1").feature().remove("seDef");
    model.sol("sol1").attach("std1");

    model.result().create("pg1", "PlotGroup3D");
    model.result("pg1").label("\u6e29\u5ea6 (ht)");
    model.result("pg1").set("data", "dset1");
    model.result("pg1").feature().create("surf1", "Surface");
    model.result("pg1").feature("surf1").label("\u8868\u9762");
    model.result("pg1").feature("surf1").set("colortable", "ThermalLight");
    model.result("pg1").feature("surf1").set("data", "parent");
    model.result().create("pg2", "PlotGroup3D");
    model.result("pg2").label("\u7b49\u6e29\u7ebf (ht)");
    model.result("pg2").set("data", "dset1");
    model.result("pg2").feature().create("iso1", "Isosurface");
    model.result("pg2").feature("iso1").label("\u7b49\u503c\u9762");
    model.result("pg2").feature("iso1").set("number", 10);
    model.result("pg2").feature("iso1").set("levelrounding", false);
    model.result("pg2").feature("iso1").set("colortable", "ThermalLight");
    model.result("pg2").feature("iso1").set("data", "parent");
    model.result().dataset("dset1").set("geom", "geom1");
    model.result().create("pg3", "PlotGroup3D");
    model.result("pg3").label("\u901f\u5ea6 (spf)");
    model.result("pg3").set("frametype", "spatial");
    model.result("pg3").set("data", "dset1");
    model.result("pg3").feature().create("slc1", "Slice");
    model.result("pg3").feature("slc1").label("\u5207\u9762");
    model.result("pg3").feature("slc1").set("expr", "spf.U");
    model.result("pg3").feature("slc1").set("smooth", "internal");
    model.result("pg3").feature("slc1").set("data", "parent");
    model.result().dataset().create("surf1", "Surface");
    model.result().dataset("surf1").label("\u5916\u58c1");
    model.result().dataset("surf1").set("data", "dset1");
    model.result().dataset("surf1").selection().geom("geom1", 2);
    model.result().dataset("surf1").selection().set(1, 2, 3, 4, 5, 6);
    model.result().dataset("surf1").selection().inherit(false);
    model.result().create("pg4", "PlotGroup3D");
    model.result("pg4").label("\u538b\u529b (spf)");
    model.result("pg4").set("frametype", "spatial");
    model.result("pg4").set("data", "surf1");
    model.result("pg4").feature().create("surf1", "Surface");
    model.result("pg4").feature("surf1").label("\u8868\u9762");
    model.result("pg4").feature("surf1").set("expr", "1");
    model.result("pg4").feature("surf1").set("titletype", "none");
    model.result("pg4").feature("surf1").set("coloring", "uniform");
    model.result("pg4").feature("surf1").set("color", "gray");
    model.result("pg4").feature("surf1").set("smooth", "internal");
    model.result("pg4").feature("surf1").set("data", "parent");
    model.result("pg4").feature().create("con1", "Contour");
    model.result("pg4").feature("con1").label("\u538b\u529b");
    model.result("pg4").feature("con1").set("expr", "p");
    model.result("pg4").feature("con1").set("number", 40);
    model.result("pg4").feature("con1").set("levelrounding", false);
    model.result("pg4").feature("con1").set("smooth", "internal");
    model.result("pg4").feature("con1").set("data", "parent");
    model.result().remove("pg2");
    model.result().remove("pg4");
    model.result().remove("pg3");
    model.result().dataset().remove("surf1");

    model.component("comp1").physics("spf").prop("PhysicalModelProperty").set("IncludeGravity", true);
    model.component("comp1").physics("spf").feature("vf1").active(false);
    model.component("comp1").physics("spf").feature().remove("vf1");
    model.component("comp1").physics("spf").prop("PhysicalModelProperty").set("UseReducedPressure", true);

    model.sol("sol1").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol1").feature().remove("t1");
    model.sol("sol1").feature().remove("v1");
    model.sol("sol1").feature().remove("st1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").feature("st1").set("study", "std1");
    model.sol("sol1").feature("st1").set("studystep", "time");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").feature("v1").set("control", "time");
    model.sol("sol1").create("t1", "Time");
    model.sol("sol1").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol1").feature("t1").set("plot", "on");
    model.sol("sol1").feature("t1").set("plotgroup", "pg1");
    model.sol("sol1").feature("t1").set("plotfreq", "tout");
    model.sol("sol1").feature("t1").set("probesel", "all");
    model.sol("sol1").feature("t1").set("probes", new String[]{});
    model.sol("sol1").feature("t1").set("probefreq", "tsteps");
    model.sol("sol1").feature("t1").set("rtol", 0.005);
    model.sol("sol1").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol1").feature("t1").set("atolglobalfactor", 0.05);
    model.sol("sol1").feature("t1").set("atolglobalvaluemethod", "factor");
    model.sol("sol1").feature("t1")
         .set("atolmethod", new String[]{"comp1_p", "scaled", "comp1_T", "global", "comp1_u", "global"});
    model.sol("sol1").feature("t1")
         .set("atol", new String[]{"comp1_p", "1e-3", "comp1_T", "1e-3", "comp1_u", "1e-3"});
    model.sol("sol1").feature("t1")
         .set("atolvaluemethod", new String[]{"comp1_p", "factor", "comp1_T", "factor", "comp1_u", "factor"});
    model.sol("sol1").feature("t1")
         .set("atolfactor", new String[]{"comp1_p", "1", "comp1_T", "0.1", "comp1_u", "0.1"});
    model.sol("sol1").feature("t1").set("endtimeinterpolation", true);
    model.sol("sol1").feature("t1").set("estrat", "exclude");
    model.sol("sol1").feature("t1").set("rhoinf", 0.5);
    model.sol("sol1").feature("t1").set("predictor", "constant");
    model.sol("sol1").feature("t1").set("maxorder", 2);
    model.sol("sol1").feature("t1").set("stabcntrl", true);
    model.sol("sol1").feature("t1").set("bwinitstepfrac", "0.01");
    model.sol("sol1").feature("t1").set("control", "time");
    model.sol("sol1").feature("t1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("t1").create("seDef", "Segregated");
    model.sol("sol1").feature("t1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d1").set("pivotperturb", 1.0E-13);

    return model;
  }

  public static Model run2(Model model) {
    model.sol("sol1").feature("t1").feature("d1")
         .label("\u76f4\u63a5\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1) (\u5df2\u5408\u5e76)");
    model.sol("sol1").feature("t1").create("i1", "Iterative");
    model.sol("sol1").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i1").set("maxlinit", 100);
    model.sol("sol1").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i1").label("AMG\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1)");
    model.sol("sol1").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("maxcoarsedof", 80000);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("strconn", 0.02);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("iter", 0);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("iter", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("fc1").set("linsolver", "d1");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").feature().remove("fcDef");
    model.sol("sol1").feature("t1").feature().remove("seDef");
    model.sol("sol1").attach("std1");

    model.component("comp1").mesh("mesh1").autoMeshSize(9);
    model.component("comp1").mesh("mesh1").run();

    model.sol("sol1").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol1").feature().remove("t1");
    model.sol("sol1").feature().remove("v1");
    model.sol("sol1").feature().remove("st1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").feature("st1").set("study", "std1");
    model.sol("sol1").feature("st1").set("studystep", "time");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").feature("v1").set("control", "time");
    model.sol("sol1").create("t1", "Time");
    model.sol("sol1").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol1").feature("t1").set("plot", "on");
    model.sol("sol1").feature("t1").set("plotgroup", "pg1");
    model.sol("sol1").feature("t1").set("plotfreq", "tout");
    model.sol("sol1").feature("t1").set("probesel", "all");
    model.sol("sol1").feature("t1").set("probes", new String[]{});
    model.sol("sol1").feature("t1").set("probefreq", "tsteps");
    model.sol("sol1").feature("t1").set("rtol", 0.005);
    model.sol("sol1").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol1").feature("t1").set("atolglobalfactor", 0.05);
    model.sol("sol1").feature("t1").set("atolglobalvaluemethod", "factor");
    model.sol("sol1").feature("t1")
         .set("atolmethod", new String[]{"comp1_p", "scaled", "comp1_T", "global", "comp1_u", "global"});
    model.sol("sol1").feature("t1")
         .set("atol", new String[]{"comp1_p", "1e-3", "comp1_T", "1e-3", "comp1_u", "1e-3"});
    model.sol("sol1").feature("t1")
         .set("atolvaluemethod", new String[]{"comp1_p", "factor", "comp1_T", "factor", "comp1_u", "factor"});
    model.sol("sol1").feature("t1")
         .set("atolfactor", new String[]{"comp1_p", "1", "comp1_T", "0.1", "comp1_u", "0.1"});
    model.sol("sol1").feature("t1").set("endtimeinterpolation", true);
    model.sol("sol1").feature("t1").set("estrat", "exclude");
    model.sol("sol1").feature("t1").set("rhoinf", 0.5);
    model.sol("sol1").feature("t1").set("predictor", "constant");
    model.sol("sol1").feature("t1").set("maxorder", 2);
    model.sol("sol1").feature("t1").set("stabcntrl", true);
    model.sol("sol1").feature("t1").set("bwinitstepfrac", "0.01");
    model.sol("sol1").feature("t1").set("control", "time");
    model.sol("sol1").feature("t1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("t1").create("seDef", "Segregated");
    model.sol("sol1").feature("t1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d1").set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("d1")
         .label("\u76f4\u63a5\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1) (\u5df2\u5408\u5e76)");
    model.sol("sol1").feature("t1").create("i1", "Iterative");
    model.sol("sol1").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i1").set("maxlinit", 100);
    model.sol("sol1").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i1").label("AMG\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1)");
    model.sol("sol1").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("maxcoarsedof", 80000);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("strconn", 0.02);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("iter", 0);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("iter", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("fc1").set("linsolver", "d1");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").feature().remove("fcDef");
    model.sol("sol1").feature("t1").feature().remove("seDef");
    model.sol("sol1").attach("std1");

    model.component("comp1").physics("spf").prop("PhysicalModelProperty").set("UseReducedPressure", false);
    model.component("comp1").physics("spf").prop("PhysicalModelProperty")
         .set("Compressibility", "CompressibleMALT03");
    model.component("comp1").physics("spf").create("prpc1", "PressurePointConstraint", 0);
    model.component("comp1").physics("spf").feature("prpc1").selection().all();

    model.sol("sol1").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol1").feature().remove("t1");
    model.sol("sol1").feature().remove("v1");
    model.sol("sol1").feature().remove("st1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").feature("st1").set("study", "std1");
    model.sol("sol1").feature("st1").set("studystep", "time");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").feature("v1").set("control", "time");
    model.sol("sol1").create("t1", "Time");
    model.sol("sol1").feature("t1").set("tlist", "range(0,0.1,10)");
    model.sol("sol1").feature("t1").set("plot", "on");
    model.sol("sol1").feature("t1").set("plotgroup", "pg1");
    model.sol("sol1").feature("t1").set("plotfreq", "tout");
    model.sol("sol1").feature("t1").set("probesel", "all");
    model.sol("sol1").feature("t1").set("probes", new String[]{});
    model.sol("sol1").feature("t1").set("probefreq", "tsteps");
    model.sol("sol1").feature("t1").set("rtol", 0.005);
    model.sol("sol1").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol1").feature("t1").set("atolglobalfactor", 0.05);
    model.sol("sol1").feature("t1").set("atolglobalvaluemethod", "factor");
    model.sol("sol1").feature("t1")
         .set("atolmethod", new String[]{"comp1_p", "scaled", "comp1_T", "global", "comp1_u", "global"});
    model.sol("sol1").feature("t1")
         .set("atol", new String[]{"comp1_p", "1e-3", "comp1_T", "1e-3", "comp1_u", "1e-3"});
    model.sol("sol1").feature("t1")
         .set("atolvaluemethod", new String[]{"comp1_p", "factor", "comp1_T", "factor", "comp1_u", "factor"});
    model.sol("sol1").feature("t1")
         .set("atolfactor", new String[]{"comp1_p", "1", "comp1_T", "0.1", "comp1_u", "0.1"});
    model.sol("sol1").feature("t1").set("endtimeinterpolation", true);
    model.sol("sol1").feature("t1").set("estrat", "exclude");
    model.sol("sol1").feature("t1").set("rhoinf", 0.5);
    model.sol("sol1").feature("t1").set("predictor", "constant");
    model.sol("sol1").feature("t1").set("maxorder", 2);
    model.sol("sol1").feature("t1").set("stabcntrl", true);
    model.sol("sol1").feature("t1").set("bwinitstepfrac", "0.01");
    model.sol("sol1").feature("t1").set("control", "time");
    model.sol("sol1").feature("t1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("t1").create("seDef", "Segregated");
    model.sol("sol1").feature("t1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d1").set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("d1")
         .label("\u76f4\u63a5\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1) (\u5df2\u5408\u5e76)");
    model.sol("sol1").feature("t1").create("i1", "Iterative");
    model.sol("sol1").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i1").set("maxlinit", 100);
    model.sol("sol1").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i1").label("AMG\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1)");
    model.sol("sol1").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("maxcoarsedof", 80000);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("strconn", 0.02);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("iter", 0);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("iter", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("fc1").set("linsolver", "d1");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").feature().remove("fcDef");
    model.sol("sol1").feature("t1").feature().remove("seDef");
    model.sol("sol1").attach("std1");
    model.sol("sol1").runAll();

    model.result("pg1").run();
    model.result().export().create("img1", "Image");
    model.result().export("img1").set("size", "current");
    model.result().export("img1").set("unit", "px");
    model.result().export("img1").set("height", "477");
    model.result().export("img1").set("width", "606");
    model.result().export("img1").set("lockratio", "off");
    model.result().export("img1").set("resolution", "96");
    model.result().export("img1").set("antialias", "on");
    model.result().export("img1").set("zoomextents", "off");
    model.result().export("img1").set("fontsize", "9");
    model.result().export("img1").set("colortheme", "globaltheme");
    model.result().export("img1").set("customcolor", new double[]{1, 1, 1});
    model.result().export("img1").set("background", "color");
    model.result().export("img1").set("gltfincludelines", "on");
    model.result().export("img1").set("title1d", "on");
    model.result().export("img1").set("legend1d", "on");
    model.result().export("img1").set("logo1d", "on");
    model.result().export("img1").set("options1d", "on");
    model.result().export("img1").set("title2d", "on");
    model.result().export("img1").set("legend2d", "on");
    model.result().export("img1").set("logo2d", "on");
    model.result().export("img1").set("options2d", "off");
    model.result().export("img1").set("title3d", "on");
    model.result().export("img1").set("legend3d", "on");
    model.result().export("img1").set("logo3d", "on");
    model.result().export("img1").set("options3d", "off");
    model.result().export("img1").set("axisorientation", "on");
    model.result().export("img1").set("grid", "on");
    model.result().export("img1").set("axes1d", "on");
    model.result().export("img1").set("axes2d", "on");
    model.result().export("img1").set("showgrid", "on");
    model.result().export("img1").set("target", "file");
    model.result().export("img1").set("qualitylevel", "92");
    model.result().export("img1").set("qualityactive", "off");
    model.result().export("img1").set("imagetype", "png");
    model.result().export("img1").set("lockview", "off");
    model.result().export().remove("img1");
    model.study("std1").feature("time").set("tlist", "range(0,1,100)");

    model.sol("sol1").study("std1");

    model.study("std1").feature("time").set("notlistsolnum", 1);
    model.study("std1").feature("time").set("notsolnum", "1");
    model.study("std1").feature("time").set("listsolnum", 1);
    model.study("std1").feature("time").set("solnum", "1");

    model.sol("sol1").feature().remove("t1");
    model.sol("sol1").feature().remove("v1");
    model.sol("sol1").feature().remove("st1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").feature("st1").set("study", "std1");
    model.sol("sol1").feature("st1").set("studystep", "time");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").feature("v1").set("control", "time");
    model.sol("sol1").create("t1", "Time");
    model.sol("sol1").feature("t1").set("tlist", "range(0,1,100)");
    model.sol("sol1").feature("t1").set("plot", "on");
    model.sol("sol1").feature("t1").set("plotgroup", "pg1");
    model.sol("sol1").feature("t1").set("plotfreq", "tout");
    model.sol("sol1").feature("t1").set("probesel", "all");
    model.sol("sol1").feature("t1").set("probes", new String[]{});
    model.sol("sol1").feature("t1").set("probefreq", "tsteps");
    model.sol("sol1").feature("t1").set("rtol", 0.005);
    model.sol("sol1").feature("t1").set("atolglobalmethod", "scaled");
    model.sol("sol1").feature("t1").set("atolglobalfactor", 0.05);
    model.sol("sol1").feature("t1").set("atolglobalvaluemethod", "factor");
    model.sol("sol1").feature("t1")
         .set("atolmethod", new String[]{"comp1_p", "scaled", "comp1_T", "global", "comp1_u", "global"});
    model.sol("sol1").feature("t1")
         .set("atol", new String[]{"comp1_p", "1e-3", "comp1_T", "1e-3", "comp1_u", "1e-3"});
    model.sol("sol1").feature("t1")
         .set("atolvaluemethod", new String[]{"comp1_p", "factor", "comp1_T", "factor", "comp1_u", "factor"});
    model.sol("sol1").feature("t1")
         .set("atolfactor", new String[]{"comp1_p", "1", "comp1_T", "0.1", "comp1_u", "0.1"});
    model.sol("sol1").feature("t1").set("endtimeinterpolation", true);
    model.sol("sol1").feature("t1").set("estrat", "exclude");
    model.sol("sol1").feature("t1").set("rhoinf", 0.5);
    model.sol("sol1").feature("t1").set("predictor", "constant");
    model.sol("sol1").feature("t1").set("maxorder", 2);
    model.sol("sol1").feature("t1").set("stabcntrl", true);
    model.sol("sol1").feature("t1").set("bwinitstepfrac", "0.01");
    model.sol("sol1").feature("t1").set("control", "time");
    model.sol("sol1").feature("t1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("t1").create("seDef", "Segregated");
    model.sol("sol1").feature("t1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("d1").set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("d1")
         .label("\u76f4\u63a5\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1) (\u5df2\u5408\u5e76)");
    model.sol("sol1").feature("t1").create("i1", "Iterative");
    model.sol("sol1").feature("t1").feature("i1").set("linsolver", "gmres");
    model.sol("sol1").feature("t1").feature("i1").set("prefuntype", "left");
    model.sol("sol1").feature("t1").feature("i1").set("itrestart", 50);
    model.sol("sol1").feature("t1").feature("i1").set("rhob", 20);
    model.sol("sol1").feature("t1").feature("i1").set("maxlinit", 100);
    model.sol("sol1").feature("t1").feature("i1").set("nlinnormuse", "on");
    model.sol("sol1").feature("t1").feature("i1").label("AMG\uff0c\u975e\u7b49\u6e29\u6d41\u52a8 (nitf1)");
    model.sol("sol1").feature("t1").feature("i1").create("mg1", "Multigrid");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("prefun", "saamg");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("mgcycle", "v");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("maxcoarsedof", 80000);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("strconn", 0.02);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("nullspace", "constant");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("usesmooth", false);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("saamgcompwise", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").set("loweramg", true);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("iter", 0);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsmethod", "lines_vertices");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("pr").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").create("sc1", "SCGS");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("linesweeptype", "ssor");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("iter", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("scgsrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsmethod", "lines_vertices");

    return model;
  }

  public static Model run3(Model model) {
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1")
         .set("scgsvertexrelax", 0.7);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("seconditer", 1);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("po").feature("sc1").set("relax", 0.5);
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").create("d1", "Direct");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("linsolver", "pardiso");
    model.sol("sol1").feature("t1").feature("i1").feature("mg1").feature("cs").feature("d1")
         .set("pivotperturb", 1.0E-13);
    model.sol("sol1").feature("t1").feature("fc1").set("linsolver", "d1");
    model.sol("sol1").feature("t1").feature("fc1").set("jtech", "once");
    model.sol("sol1").feature("t1").feature("fc1").set("damp", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("ntolfact", 0.5);
    model.sol("sol1").feature("t1").feature("fc1").set("stabacc", "aacc");
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdim", 5);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccmix", 0.9);
    model.sol("sol1").feature("t1").feature("fc1").set("aaccdelay", 1);
    model.sol("sol1").feature("t1").feature("fc1").set("maxiter", 8);
    model.sol("sol1").feature("t1").feature().remove("fcDef");
    model.sol("sol1").feature("t1").feature().remove("seDef");
    model.sol("sol1").attach("std1");
    model.sol("sol1").runAll();

    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").create("iso1", "Isosurface");
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").run();
    model.result("pg1").feature().remove("iso1");
    model.result("pg1").run();
    model.result().create("pg2", "PlotGroup3D");
    model.result("pg2").run();
    model.result("pg2").create("iso1", "Isosurface");
    model.result("pg1").run();
    model.result("pg2").run();
    model.result("pg2").label("\u7b49\u6e29\u9762");
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").selection().geom("geom1", 3);
    model.result("pg2").selection().geom("geom1", 3);
    model.result("pg2").selection().set(1);
    model.result("pg2").selection().geom("geom1", 3);
    model.result("pg2").selection().all();
    model.result("pg2").run();
    model.result("pg2").selection().inherit(false);
    model.result("pg2").selection().geom("geom1");
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 1, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 2, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 3, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 4, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 5, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 6, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 7, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 8, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 9, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 10, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 11, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 12, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 13, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 14, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 15, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 16, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 1, 0);
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").feature("iso1").set("number", 20);
    model.result("pg2").run();
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 2, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 3, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 4, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 5, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 6, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 7, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 8, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 9, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 10, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 11, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 12, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 13, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 14, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 15, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 16, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 17, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 18, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 19, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 20, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 21, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 22, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 23, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 24, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 25, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 26, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 27, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 28, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 29, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 30, 0);
    model.result("pg2").run();
    model.result("pg2").setIndex("looplevel", 31, 0);
    model.result("pg2").run();
    return model;
  }

  public static void main(String[] args) {
    Model model = run();
    model = run2(model);
    run3(model);
  }

}
