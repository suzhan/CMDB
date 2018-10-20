<template>
    <div class="single-input-dialog" v-if="visible" style="background-image:url('../assets/light-main-bg.png');width:100%;
        height:100px;">
        <el-dialog
            title=""
            :visible.sync="open"
            :show-close="true"
            width="50%"
            :before-close="handleClose"
            center>
            <el-tabs >
              <el-tab-pane label="阿里云帐号">
                  <el-form :show-message="false" :inline="true" :model="cloudForm" :rules="cloudFormRules" ref="cloudForm" >
                      <el-form-item label="" prop="cloud_account_name">
                          <el-input  v-model="cloudForm.cloud_account_name" :placeholder="label" ></el-input>
                      </el-form-item>
                      <el-form-item>
                          <el-button type="primary" @click="fnAddCloudMaster('cloudForm')">添加</el-button>
                      </el-form-item>
                  </el-form>
              </el-tab-pane>
              <el-tab-pane label="物理主机">
                  <el-form :show-message="false" label-width="200px" :model="localForm" :rules="localFormRules" ref="localForm" >
                      <el-form-item label="名称" prop="localForm_name" >
                         <el-input v-model="localForm.localForm_name" ></el-input>
                      </el-form-item>
                      <el-form-item label="IP地址" prop="localForm_pri_ip">
                         <el-input v-model="localForm.localForm_pri_ip"></el-input>
                      </el-form-item>
                      <el-form-item label="CPU" prop="localForm_cpu">
                         <el-input v-model="localForm.localForm_cpu"></el-input>
                      </el-form-item>
                      <el-form-item label="内存" prop="localForm_mem">
                         <el-input v-model="localForm.localForm_mem"></el-input>
                      </el-form-item>
                      <el-form-item label="系统分区" prop="localForm_device_sys">
                         <el-input v-model="localForm.localForm_device_sys"></el-input>
                      </el-form-item>
                      <el-form-item label="系统分区大小" prop="localForm_device_sys_size">
                         <el-input v-model="localForm.localForm_device_sys_size"></el-input>
                      </el-form-item>
                      <el-form-item label="数据分区" prop="localForm_device_data">
                         <el-input v-model="localForm.localForm_device_data"></el-input>
                      </el-form-item>
                      <el-form-item label="数据分区大小" prop="localForm_device_data_size">
                         <el-input v-model="localForm.localForm_device_data_size"></el-input>
                      </el-form-item>
                      <el-form-item label="操作系统" prop="localForm_os">
                          <el-input v-model="localForm.localForm_os"></el-input>
                      </el-form-item>
                      <el-form-item label="状态" prop="localForm_status">
                         <el-input v-model="localForm.localForm_status" ></el-input>
                      </el-form-item>
                      <el-form-item>
                          <el-button type="primary" @click="fnAddLocalMaster('localForm')">添加</el-button>
                      </el-form-item>
                  </el-form>
              </el-tab-pane>
            </el-tabs>

        </el-dialog>
        <div>
            <slot name="customContent"></slot>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "AddMasterDialog",
        props: {
            visible: {
                type: Boolean,
                required: true
            },
            label: {
                type: String,
                defalut: '',
            }
        },
        data() {
            return {
                open: false,

                cloudForm: {
                    cloud_account_name: ''
                },
                localForm: {
                    localForm_name: '',
                    localForm_pri_ip: '',
                    localForm_cpu: '',
                    localForm_mem: '',
                    localForm_device_sys: '',
                    localForm_device_sys_size: '',
                    localForm_device_data: '',
                    localForm_device_data_size: '',
                    localForm_os: '',
                    localForm_status: ''
                },
                cloudFormRules: {
                    cloud_account_name: [
                        {required: true, message: '', trigger: 'change'}
                    ]
                },
                localFormRules: {
                    localForm_name: [
                         {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_pri_ip: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_cpu: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_mem: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_device_sys: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_device_sys_size: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_device_data: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_device_data_size: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_os: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    localForm_status: [
                        {required: true, message: '', trigger: 'change'}
                    ]
                }
            }
        },
        watch: {
            visible: function (newVal, oldVal) {
                if(newVal) {
                    this.open = true;
                }

            }
        },
        methods: {
            fnAddCloudMaster: function (cloudForm) {
                this.$refs[cloudForm].validate((valid) => {
                    if (valid) {
                        console.log('云端帐号',this.cloudForm.cloud_account_name);

                        axios.post('api/add_cloud_master', {
                            cloud_account_name: this.cloudForm.cloud_account_name
                        }).then(response => {
                            console.log(response);
                            this.$alert(response.data.resultMsg[0], '信息', {
                                confirmButtonText: '确定',
                                type: response.data.resultCode[0],
                            });
                        })
                        // this.$emit('addCloudMasterCallback', this.form)
                    } else {
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                })
            },
            fnAddLocalMaster: function (localForm) {
                this.$refs[localForm].validate((valid) => {
                    if (valid) {
                        console.log('本地宿主',this.localForm);
                        axios.post('api/add_local_master', {
                            localForm: this.localForm
                        }).then(response => {
                            console.log(response);
                            this.$alert(response.data.resultMsg[0], '信息', {
                                confirmButtonText: '确定',
                                type: response.data.resultCode[0],
                            });
                        })
                        // this.$emit('addLocalMasterCallback', this.form)
                    } else {
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                })
            },
            handleClose(done) {
                this.$emit('closeMasterCallback', false);
                done();
            }
        },
        mounted() {
            this.open = true;
        }
    }
</script>

<style scoped>
     /*控制表单行距*/
    .el-form-item {margin-bottom: 7px;}
    .el-input {width: 300px}

</style>