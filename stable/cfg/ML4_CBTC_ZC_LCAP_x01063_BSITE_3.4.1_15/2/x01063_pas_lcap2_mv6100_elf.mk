#LCAP ID
LCAP=lcap2

#TECHNO ID
TECH=../tech_ppc_mvme6100
MODELE=ppc_mvme6100_relf.mk

#SERVER ID
HOSTNAME=LOAD_BALANCING

#SIGNATURE ID
VCF=x01063_pas_parametrage.vcf

#=======================================================================
#DIRECTORIES WHERE TO LOOK FOR THE LIBRARIES
#=======================================================================

DIRS= \
../csd_lcap_mvme6100_liv \
../cbtczc_00lcap_mvme6100 \
../x01063_bch \
../x01063capx_mvme6100 \

#=======================================================================
#CSD LIBRARIES (!! Please do not change this part !!)
#=======================================================================

#WINDRIVER PROJECT FILE
#----------------------

WPJ=VIP_CSD_PPC_MV6100.wpj

#CSD Source code
#---------------

LIBS_SRCS_CSD= \
lib_srcs_lcapx_bsp_vxw_mvme6100.tgz \
lib_srcs_lcapx_bsp_mvme6100.tgz \
lib_srcs_lcapx_cst_mvme6100.tgz \
lib_srcs_lcapx_csd_mvme6100.tgz \

LIB_OBJS_CSD= \
lib_objs_lcapx_csd_at_mvme6100.a \
libPPC604gnatvx_nomorealloc_patch.a \

#CSD Production
#--------------

LIB_SRCS_CSD_PRO=lib_srcs_$(LCAP)_pro_mvme6100.tgz

#CSD Configuration
#-----------------

LIB_SRCS_CSD_CNF=lib_srcs_$(LCAP)_csd_cnf_mvme6100.tgz

#=======================================================================
# APPLICATION LIBRARIES
#=======================================================================

# APP Source code. 
#-----------------

# The TGZS_APP macro must be used to declare all the application libraries 
# for LCAP 1, 2 and 3.

# The ADA specifications "csd_conf_genere" and the "csd_lcap_conf_genere" 
# produced by the CSD configuration tool must be provided to the compilation
# toolchain through this macro. In the example below below these two ADA 
# specification are provided separately by means of a dedicated library
# called "lib_srcs_lcapx_app_csd_cnf_mvme6100.tgz".

LIBS_SRCS_APP= \
x01063_pas_lcapx_src_param.tgz \
x01063_pas_src_capx.tgz \
\
pas_src_cfg.tgz \
pas_src_com.tgz \
pas_src_pasapp.tgz \
pas_src_pascfg.tgz \
pas_src_pascom.tgz \
pas_src_paspre.tgz

# APP Objects libraries 
#-----------------------

# The user can declare it owns object libraries.

LIBS_OBJS_APP=LIB_OBJS_SCADE.a

# APP Configuration
#------------------

# The TGZS_APP_CNF macro must be used to declare a single library containing
# the configuration aspects for a specific LCAP (identified by macro "LCAP").
#
# It should contain at least :
#   - The PROM identification key from the production tool.
#   - The SACEM LC signatures.	

LIB_SRCS_APP_CNF=x01063_pas_$(LCAP)_src_param.tgz

