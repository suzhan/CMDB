<template>
    <div class="addDatabaseDialog" v-if="visible">
        <el-dialog
            title=""
            :visible.sync="open"
            :show-close="true"
            width="450px"
            :before-close="handleClose"
            center>
                <el-form :show-message="false"  label-width="100px" :model="form" :rules="formRules" ref="form" >
                    <el-form-item label="数据库名" prop="form_name">
                        <el-input  v-model="form.form_name"></el-input>
                    </el-form-item>
                     <el-form-item label="用户名" prop="form_user">
                        <el-input  v-model="form.form_user"></el-input>
                    </el-form-item>
                    <el-form-item label="数据库类" prop="form_databases_type">
                        <el-select v-model="form.form_databases_type" filterable placeholder="请选择数据类别">
                            <el-option
                                v-for="item in databases_type_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="fnAddNew('form')">添加</el-button>
                    </el-form-item>
                </el-form>
        </el-dialog>
    </div>
</template>

<script>

    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "addDatabaseDialog",
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
                databases_type_options: [],
                form_databases_type: [],
                form: {
                    form_name: '',
                    form_user: '',
                    form_databases_type: []
                },
                formRules: {
                    form_name: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    form_user: [
                        {required: true, message: '', trigger: 'change'}
                    ],
                    form_databases_type: [
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
            fnAddNew: function (form) {
                this.$refs[form].validate((valid) => {
                    if (valid) {
                        axios.post('api/add_new_database', {
                            form: this.form
                        }).then(response => {
                            console.log(response);
                            this.$alert(response.data.resultMsg[0], '信息', {
                                 confirmButtonText: '确定',
                                 type: response.data.resultCode[0],
                            });
                        })
                        // this.$emit('addBranchCallback', this.form)
                    } else {
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                })
            },
            fnGetRequest() {
                axios.get('/api/software')
                .then(response => {
                    console.log(response);
                    this.databases_type_options = response.data.databases_type_options;
                })
            },
            handleClose(done) {
                this.$emit('closeCallback', false);
                done();
            }
        },
        mounted() {
            this.fnGetRequest();
            this.open = true;
        }
    }
</script>

<style scoped>
    .el-input {width: 220px}
</style>