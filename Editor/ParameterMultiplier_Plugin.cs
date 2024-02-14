using elkies.parametermultiplier;
using UnityEngine;
using UnityEditor.Animations;
using VRC.SDK3.Avatars.Components;
using System.Collections.Generic;
using System.Linq;

using nadena.dev.modular_avatar.core;
using nadena.dev.ndmf;
using VRC.SDKBase;

[assembly: ExportsPlugin(typeof(ParameterMultiplier_Plugin))]

namespace elkies.parametermultiplier {
    public class ParameterMultiplier_Plugin : Plugin<ParameterMultiplier_Plugin> {
        protected override void Configure() {
            List<string> listOfWords = null;
            string ParameterIdentifier = null;
            string ParameterMultiplierIndexVariableName = null;
            string ParameterMultiplierValueVariableName = null;
            string ParameterMultiplierFXLayerName = null;

            InPhase(BuildPhase.Generating).Run("Generate Animator for Multiple Parameters", ctx => {
                var ParameterMultiplier = ctx.AvatarRootObject.GetComponentInChildren<ParameterMultiplier>(); ;

                if(ParameterMultiplier == null) { return; }

                ParameterIdentifier = ParameterMultiplier.GetParamterIdentifier();
                ParameterMultiplierIndexVariableName = $"{ParameterIdentifier}/{ParameterMultiplier.GetParameterMultiplierIndexVariableName()}";
                ParameterMultiplierValueVariableName = $"{ParameterIdentifier}/{ParameterMultiplier.GetParameterMultiplierValueVariableName()}";
                ParameterMultiplierFXLayerName = ParameterMultiplier.GetParameterMultiplierFXLayerName();

                listOfWords = new List<string>(ParameterMultiplier.ParameterList.text.Split("\n").Select(x => x.TrimEnd()));
                var AnimatorControllerVar = new AnimatorController();
                AnimatorControllerVar.AddParameter(ParameterMultiplierIndexVariableName, AnimatorControllerParameterType.Int);
                AnimatorControllerVar.AddParameter(ParameterMultiplierValueVariableName, AnimatorControllerParameterType.Int);
                AnimatorControllerVar.AddParameter("IsLocal", AnimatorControllerParameterType.Bool);
                AnimatorControllerVar.AddLayer(ParameterMultiplierFXLayerName);

                var RootStateMachine = AnimatorControllerVar.layers[0].stateMachine;

                var MergeAnimator = ParameterMultiplier.gameObject.AddComponent<ModularAvatarMergeAnimator>(); ;
                var MAParameters = ParameterMultiplier.gameObject.GetOrAddComponent<ModularAvatarParameters>();

                var WaitTransition = RootStateMachine.AddAnyStateTransition(RootStateMachine.AddState("Wait"));
                WaitTransition.AddCondition(AnimatorConditionMode.Equals, 0, ParameterMultiplierIndexVariableName);
                WaitTransition.duration = 0;
                WaitTransition.exitTime = 0;
                WaitTransition.canTransitionToSelf = false;

                MAParameters.parameters.Add(new ParameterConfig {
                    nameOrPrefix = ParameterMultiplierIndexVariableName,
                    syncType = ParameterSyncType.Int,
                    localOnly = false,
                    saved = false
                });

                MAParameters.parameters.Add(new ParameterConfig {
                    nameOrPrefix = ParameterMultiplierValueVariableName,
                    syncType = ParameterSyncType.Int,
                    localOnly = false,
                    saved = false
                });

                foreach (var x in listOfWords.Select((string Temp, int index) => (Temp, index))) {
                    var index = x.index + 1;
                    var ParameterName = x.Temp.Split(",")[0];
                    var ParameterType = x.Temp.Split(",")[1];

                    var TempState = RootStateMachine.AddState($"Receive_{ParameterName}");

                    AnimatorControllerVar.AddParameter(GetAnimatorControllerParameter(ParameterName, ParameterType));

                    MAParameters.parameters.Add(new ParameterConfig {
                        nameOrPrefix = $"{ParameterIdentifier}/{ParameterName}|{index}",
                        syncType = ParameterSyncType.Bool,
                        localOnly = true,
                        saved = false
                    });

                    var TempParameterDriver = TempState.AddStateMachineBehaviour<VRCAvatarParameterDriver>();
                    TempParameterDriver.parameters = GetParameterDriver_Parameter(ParameterMultiplierValueVariableName, ParameterName, ParameterType);

                    var TempTransition = RootStateMachine.AddAnyStateTransition(TempState);
                    TempTransition.AddCondition(AnimatorConditionMode.Equals, index, ParameterMultiplierIndexVariableName);
                    TempTransition.AddCondition(AnimatorConditionMode.IfNot, 0.0f, "IsLocal");
                    TempTransition.duration = 0;
                    TempTransition.exitTime = 0.01f;
                }

                MergeAnimator.animator = AnimatorControllerVar;
                MergeAnimator.layerType = VRCAvatarDescriptor.AnimLayerType.FX;
                MergeAnimator.pathMode = MergeAnimatorPathMode.Absolute;
                MergeAnimator.matchAvatarWriteDefaults = true;

            });
        }


        private List<VRC_AvatarParameterDriver.Parameter> GetParameterDriver_Parameter(string Source, string Target, string TargetType) {
            if (TargetType == "float") {
                return new List<VRC_AvatarParameterDriver.Parameter> {
                            new VRC_AvatarParameterDriver.Parameter {
                                type = VRC_AvatarParameterDriver.ChangeType.Copy,
                                source = Source,
                                name = Target,
                                convertRange = true,
                                sourceMin = 0.0f,
                                sourceMax = 254.0f,
                                destMin = -1.0f,
                                destMax = 1.0f
    }
                        };
            } else {
                return new List<VRC_AvatarParameterDriver.Parameter> {
                            new VRC_AvatarParameterDriver.Parameter {
                                type = VRC_AvatarParameterDriver.ChangeType.Copy,
                                source = Source,
                                name = Target
                            }
                        };
            }
        }

        private AnimatorControllerParameter GetAnimatorControllerParameter(string ParameterName, string Type) {
            var tempString = Type.ToUpper();
            if (tempString == "FLOAT") {
                return new AnimatorControllerParameter {
                    name = ParameterName,
                    type = AnimatorControllerParameterType.Float
                };
            } else if (tempString == "BOOL") {
                return new AnimatorControllerParameter {
                    name = ParameterName,
                    type = AnimatorControllerParameterType.Bool
                };
            } else {
                return new AnimatorControllerParameter {
                    name = ParameterName,
                    type = AnimatorControllerParameterType.Int
                };
            }
        }
    }
}