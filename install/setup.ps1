# generated from colcon_powershell/shell/template/prefix_chain.ps1.em

# This script extends the environment with the environment of other prefix
# paths which were sourced when this file was generated as well as all packages
# contained in this prefix path.

# function to source another script with conditional trace output
# first argument: the path of the script
function _colcon_prefix_chain_powershell_source_script {
  param (
    $_colcon_prefix_chain_powershell_source_script_param
  )
  # source script with conditional trace output
  if (Test-Path $_colcon_prefix_chain_powershell_source_script_param) {
    if ($env:COLCON_TRACE) {
      echo ". '$_colcon_prefix_chain_powershell_source_script_param'"
    }
    . "$_colcon_prefix_chain_powershell_source_script_param"
  } else {
    Write-Error "not found: '$_colcon_prefix_chain_powershell_source_script_param'"
  }
}

# source chained prefixes
_colcon_prefix_chain_powershell_source_script "/opt/ros/humble\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/test/hanumanoid_interaction/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/isaac_ws/Isaacsim_ros2_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/whaly_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/moveit_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/Downloads/URDF_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/rl_ws/rl_sar-main/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/ros2_addons_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/hanumanoid_ws/hanumanoid_ros2_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/urdf_generator_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/ws_moveit2/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/whaly/hanumanoid_interaction_ws/hanumanoid_interaction_ros_ws/install\local_setup.ps1"

# source this prefix
$env:COLCON_CURRENT_PREFIX=(Split-Path $PSCommandPath -Parent)
_colcon_prefix_chain_powershell_source_script "$env:COLCON_CURRENT_PREFIX\local_setup.ps1"
