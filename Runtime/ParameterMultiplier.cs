using UnityEngine;
using VRC.SDKBase;

namespace elkies.parametermultiplier
{
    public class ParameterMultiplier : MonoBehaviour, IEditorOnly
    {
        private string ParameterMultiplierFXLayerName = "ParameterMultiplier";
        private string ParameterIdentifier = "ParameterMultiplier";
        private string ParameterMultiplierIndexVariableName = "PM_INX";
        private string ParameterMultiplierValueVariableName = "PM_VAL";

        public TextAsset ParameterList;

        public string GetParamterIdentifier () { return ParameterIdentifier; }
        public string GetParameterMultiplierIndexVariableName() { return ParameterMultiplierIndexVariableName; }
        public string GetParameterMultiplierValueVariableName() { return ParameterMultiplierValueVariableName; }
        public string GetParameterMultiplierFXLayerName() { return ParameterMultiplierFXLayerName; }
    }
}
