<template>
    <el-tabs type="border-card" >
        <el-tab-pane>
            <span slot="label"><i class="el-icon-date"></i> 概览</span>
                <el-row>
                    <el-col>
                        <div style="float: right;" >
                            <el-select @change="fnBranchChange" v-model="branch_value" filterable placeholder="请选择分支">
                               <el-option
                                     v-for="item in branch_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select @change="fnSoftwareTypeChange" v-model="software_type_value" style="margin-left: 20px;" filterable placeholder="请选择应用类别">
                                <el-option
                                  v-for="item in software_type_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col>
                        <el-table :data="tableData" stripe medium style="width: 100%; margin-top: 20px">
                            <el-table-column type="index" width="50"></el-table-column>
                            <el-table-column prop="name" label="名称" width="180"></el-table-column>
                            <el-table-column prop="pri_ip" label="私有IP" width="120"></el-table-column>
                            <el-table-column prop="cpu" label="CPU" width="60"></el-table-column>
                            <el-table-column prop="mem" label="内存" width="80"></el-table-column>
                            <el-table-column prop="device_sys" label="系统分区" ></el-table-column>
                            <el-table-column prop="device_sys_size" label="系统大小" width="100"></el-table-column>
                            <el-table-column prop="device_data" label="数据分区" ></el-table-column>
                            <el-table-column prop="device_data_size" label="数据大小" width="100"></el-table-column>
                            <el-table-column prop="os" label="操作系统" width="150"></el-table-column>
                            <el-table-column prop="status" label="状态" ></el-table-column>
                            <el-table-column label="操作" width="160">
                              <template slot-scope="scope">
                                <el-button
                                  size="mini"
                                  @click="handleEdit(scope.$index, scope.row)">状态</el-button>
                                <el-button
                                  size="mini"
                                  type="danger"
                                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                              </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-tab-pane>
        <!--数据编辑-->
        <el-tab-pane  >
            <span slot="label"><i class="el-icon-edit"></i> 编辑</span>
            <!--查询表单-->
            <el-row>
                <el-col :span="10">
                    <!--<div class="grid-content bg-purple-dark">-->
                        <!--<el-input placeholder="请输入私有IP地址进行搜索" v-model="node_search" @keyup.enter.native="node_search_submit">-->
                            <!--<i slot="prefix" class="el-input__icon el-icon-search"></i>-->
                        <!--</el-input>-->
                    <!--</div>-->
                    <el-select @change="node_search_submit" v-model="node_search" filterable placeholder="搜索">
                                <el-option
                                  v-for="item in node_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                  </el-col>
            </el-row>
            <!--表单开始-->
            <el-form  :show-message="false"  ref="nodeForm" :model="nodeForm"  :rules="nodeRules"  label-width="280px" style="margin-top: 20px" >
                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="名称" prop="nodeForm_name" >
                            <el-input v-model="nodeForm.nodeForm_name" ></el-input>
                        </el-form-item>
                    </el-col>

                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="所属主机类别" prop="nodeForm_node_type" >
                            <el-select v-model="nodeForm.nodeForm_node_type"  filterable placeholder="请选择主机类别">
                                <el-option
                                  v-for="item in node_type_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddNodeTypeDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                <!--调用components共用资源-->
                <addNodeTypeDialog
                        :visible="addNodeTypeDialogVisible"
                        label="请输入新主机类别"
                        @closeCallback="fnNodeTypeCloseDialog"
                        @addNodeTypeCallback="fnAddNodeType">
                </addNodeTypeDialog>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="IP地址" prop="nodeForm_pri_ip">
                            <el-input v-model="nodeForm.nodeForm_pri_ip"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" >
                        <!--所属于分支-->
                        <el-form-item label="所属分支 -->"  prop="nodeForm_branch" >
                            <el-select v-model="nodeForm.nodeForm_branch" value-key="value" multiple filterable placeholder="请选择所属于分支">
                                <el-option
                                     v-for="item in branch_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddBranchDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                 <!--调用components共用资源--新分支-->
                <addBranchDialog
                        :visible="addBranchDialogVisible"
                        label="请输入新分支"
                        @closeCallback="fnBranchCloseDialog">
                        <!--@addBranchCallback="fnAddBranch">-->
                </addBranchDialog>


                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="CPU" prop="nodeForm_cpu">
                            <el-input v-model="nodeForm.nodeForm_cpu"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10">
                        <!--所属于主机-->
                        <el-form-item label="所属主机 -->" prop="nodeForm_master">
                            <el-select v-model="nodeForm.nodeForm_master" value-key="value" multiple filterable placeholder="请选择所属于主机">
                                 <el-option
                                  v-for="item in master_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddMasterDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                <!--调用components共用资源--新主机或阿里号-->
                <addMasterDialog
                        :visible="addMasterDialogVisible"
                        label="请输入新主机或阿里号"
                        @closeMasterCallback="fnMasterCloseDialog"
                        @addMasterCallback="fnAddMaster">
                </addMasterDialog>

                <el-row type="flex" >
                    <el-col :span="10">
                         <el-form-item label="内存" prop="nodeForm_mem">
                             <el-input v-model="nodeForm.nodeForm_mem"></el-input>
                         </el-form-item>
                    </el-col>
                    <el-col :span="10" >
                        <!--所属于业务线-->
                        <el-form-item label="所属业务线 -->" prop="nodeForm_business_line">
                            <el-select v-model="nodeForm.nodeForm_business_line" multiple filterable placeholder="请选择所属业务线">
                                 <el-option
                                  v-for="item in business_line_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenBusinessLineDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                 <!--调用components共用资源--新业务线-->
                <addBusinessLineDialog
                        :visible="addBusinessLineDialogVisible"
                        label="请输入新业务线"
                        @closeCallback="fnBusinessLineCloseDialog"
                        @addBusinessLineCallback="fnAddBusinessLine">
                </addBusinessLineDialog>


                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="系统分区" prop="nodeForm_device_sys">
                            <el-input v-model="nodeForm.nodeForm_device_sys"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="系统分区大小" prop="nodeForm_device_sys_size">
                            <el-input v-model="nodeForm.nodeForm_device_sys_size"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                         <el-form-item label="数据分区" prop="nodeForm_device_data">
                             <el-input v-model="nodeForm.nodeForm_device_data"></el-input>
                         </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="数据分区大小" prop="nodeForm_device_data_size">
                            <el-input v-model="nodeForm.nodeForm_device_data_size"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="操作系统" prop="nodeForm_os">
                            <el-input v-model="nodeForm.nodeForm_os"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="状态" prop="nodeForm_status">
                            <el-input v-model="nodeForm.nodeForm_status" ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" style="margin-left: 60px;"></el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="24">
                        <el-form-item style="margin-left: 280px;margin-top: 20px">
                            <el-button type="primary" @click="submitForm('nodeForm')">立即创建</el-button>
                            <el-button @click="resetForm('nodeForm')">重置</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>

            </el-form>
        </el-tab-pane>
    </el-tabs>
</template>





<script>

    const axios = require('axios');

    // var axiosDefaults = require("axios/lib/defaults");
    // axiosDefaults.xsrfCookieName = "csrftoken";
    // axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    // axiosDefaults.withCredentials = true;


    // import axios from 'axios'
    // // 拦截request,设置全局请求为ajax请求
    axios.interceptors.request.use((config) => {
      config.headers['X-Requested-With'] = 'XMLHttpRequest';
      let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
      config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
      return config
    });


    import addNodeTypeDialog from '@/components/addNodeTypeDialog';
    import addBranchDialog from '@/components/addBranchDialog';
    import addBusinessLineDialog from '@/components/addBusinessLineDialog';
    import addMasterDialog from '@/components/addMasterDialog';


    export default {
        data() {
            return {

                computer_type: null,
                addNodeTypeForm: null,

                addNodeTypeDialogVisible: false,
                addBusinessLineDialogVisible: false,
                addBranchDialogVisible: false,
                addMasterDialogVisible: false,

                new_node_type: null,

                branch_options: null,
                software_type_options: null,
                business_line_options: null,
                master_options: null,
                node_type_options: null,

                branch_value: null,
                software_type_value: null,

                nodeForm_branch: [],
                nodeForm_master: [],
                nodeForm_business_line: [],

                branch_result: [],
                master_result: [],
                business_line_result: [],
                nodeForm_software_type: [],

                node_options: [],

                tableData: null,

                node_search: null,

                nodeForm: {
                    nodeForm_name: '',
                    nodeForm_pri_ip: '',
                    nodeForm_cpu: '',
                    nodeForm_mem: '',
                    nodeForm_device_sys: '',
                    nodeForm_device_sys_size: '',
                    nodeForm_device_data: '',
                    nodeForm_device_data_size: '',
                    nodeForm_os: '',
                    nodeForm_status: '',

                    branch_result: [],
                    master_result: [],
                    business_line_result: [],
                    nodeForm_software_type: [],
                    nodeForm_node_type: '',
                },

                nodeRules:{
                    nodeForm_name: [
                      { required: true, message: '请输入主机名称', trigger: 'change' }
                    ],
                    nodeForm_pri_ip: [
                      { required: true, message: '请输入私有IP', trigger: 'change' }
                    ],
                    nodeForm_cpu: [
                      { required: true, message: '请输入CPU', trigger: 'change' }
                    ],
                    nodeForm_mem: [
                      { required: true, message: '请输入内存', trigger: 'change' }
                    ],
                    nodeForm_device_sys: [
                      { required: true, message: '请输入系统分区名', trigger: 'change' }
                    ],
                    nodeForm_device_sys_size: [
                      { required: true, message: '请输入系统分区大小', trigger: 'change' }
                    ],
                    nodeForm_device_data: [
                      { required: true, message: '请输入数据分区名', trigger: 'change' }
                    ],
                    nodeForm_device_data_size: [
                      { required: true, message: '请输入数据分区大小', trigger: 'change' }
                    ],
                    nodeForm_os: [
                      { required: true, message: '请输入操作系统', trigger: 'change' }
                    ],
                    nodeForm_status: [
                      { required: true, message: '请输入主机状态', trigger: 'change' }
                    ],
                    nodeForm_branch: [
                      { required: true, message: '请属于分支', trigger: 'change' }
                    ],
                    nodeForm_master: [
                      { required: true, message: '请属于主机', trigger: 'change' }
                    ],
                    nodeForm_business_line: [
                      { required: true, message: '请属于业务线', trigger: 'change' }
                    ],
                    nodeForm_software_type: [
                      { required: true, message: '请选择软件类别', trigger: 'change' }
                    ],
                    nodeForm_node_type: [
                      { required: true, message: '请选择主机类别', trigger: 'change' }
                    ]
                },
                addNodeTypeForm:{
                    new_node_type: ''
                }
            }
        },
        methods: {
            fnOpenBusinessLineDialog() {
                this.addBusinessLineDialogVisible = true;
            },
            fnBusinessLineCloseDialog(status) {
                console.log('visible status', status);
                this.addBusinessLineDialogVisible = status;
            },

            fnOpenAddNodeTypeDialog() {
                this.addNodeTypeDialogVisible = true;
            },
            fnNodeTypeCloseDialog(status) {
                console.log('visible status', status);
                this.addNodeTypeDialogVisible = status;
            },


            fnOpenAddBranchDialog() {
                this.addBranchDialogVisible = true;
            },
            fnBranchCloseDialog(status) {
                console.log('visible status', status);
                this.addBranchDialogVisible = status;
            },


            fnOpenAddMasterDialog() {
                this.addMasterDialogVisible = true;
            },
            fnMasterCloseDialog(status) {
                console.log('visible status', status);
                this.addMasterDialogVisible = status;
            },



            fnBranchChange() {
                console.log(this.branch_value);

                axios.post('/api/node', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.tableData = response.data.node
                })
            },
            fnSoftwareTypeChange() {
                console.log(this.software_type_value);

                axios.post('/api/node', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.tableData = response.data.node
                })
            },
            fnGetRequest() {
                axios.get('/api/node')
                .then(response => {
                    console.log(response);
                    this.branch_options = response.data.branch_options;
                    this.software_type_options = response.data.software_type_options;
                    this.master_options = response.data.master_options;
                    this.business_line_options = response.data.business_line_options;
                    this.node_type_options = response.data.node_type_options;
                    this.node_options = response.data.node_options;
                });
            },
            submitForm: function (nodeForm) {
                this.$refs[nodeForm].validate((valid) => {
                    if (valid) {
                        axios.post('/api/node', {
                            nodeForm: this.nodeForm
                        }).then(response => {
                            console.log(response);
                            // 信息弹窗口
                            this.$alert(response.data.resultMsg[0], '信息', {
                                confirmButtonText: '确定',
                                type: response.data.resultCode[0],
                            });
                        })
                    } else {
                        console.log('error submit!!');
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                });
            },
            resetForm(nodeForm) {
                this.$refs[nodeForm].resetFields();
                this.node_search = '';
            },
            node_search_submit() {
                axios.post('/api/node', {
                node_search: this.node_search
                }).then(response => {
                    console.log(response);
                    this.nodeForm.nodeForm_name = response.data.node_search[0].name;
                    this.nodeForm.nodeForm_pri_ip = response.data.node_search[0].pri_ip;
                    this.nodeForm.nodeForm_cpu = response.data.node_search[0].cpu;
                    this.nodeForm.nodeForm_mem = response.data.node_search[0].mem;
                    this.nodeForm.nodeForm_device_sys = response.data.node_search[0].device_sys;
                    this.nodeForm.nodeForm_device_sys_size = response.data.node_search[0].device_sys_size;
                    this.nodeForm.nodeForm_device_data = response.data.node_search[0].device_data;
                    this.nodeForm.nodeForm_device_data_size = response.data.node_search[0].device_data_size;
                    this.nodeForm.nodeForm_os = response.data.node_search[0].os;
                    this.nodeForm.nodeForm_status = response.data.node_search[0].status;
                    // 三个多选框
                    this.nodeForm.nodeForm_branch = response.data.branch_result;
                    this.nodeForm.nodeForm_master = response.data.master_result;
                    this.nodeForm.nodeForm_business_line = response.data.business_line_result;
                    // 主机类别
                    this.nodeForm.nodeForm_node_type = response.data.node_type_result[0];
                })
            },
            fnAddNodeType(data) {
                console.log('接受新主机类的数据',data);
                axios.post('/api/add_node_type', {
                    single_input_text: data.single_input_text
                }).then(response => {
                    console.log(response);
                    this.$alert(response.data.resultMsg[0], '信息', {
                         confirmButtonText: '确定',
                         type: response.data.resultCode[0],
                    });
                })
            },
            fnAddBusinessLine(data) {
                console.log('接受新业务线的数据',data);
                axios.post('/api/add_new_business_line', {
                    single_input_text: data.single_input_text
                }).then(response => {
                    console.log(response);
                    this.$alert(response.data.resultMsg[0], '信息', {
                         confirmButtonText: '确定',
                         type: response.data.resultCode[0],
                    });
                })
            },
            fnAddMaster(){
                console.log('接受主机或阿里云的数据',data);
            }
        },
        mounted() {
            this.fnGetRequest()
        },
        components: {
            addNodeTypeDialog,
            addBranchDialog,
            addBusinessLineDialog,
            addMasterDialog
        }
    }
</script>

<style lang="scss" scoped>
     /*控制表单行距*/
    .el-form-item {margin-bottom: 10px;}
</style>