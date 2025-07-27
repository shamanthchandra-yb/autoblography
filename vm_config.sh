#!/bin/bash

# VM Configuration for AutoBlography Deployment
# Copy this file and update with your actual VM details

# VM Connection Details
export VM_USER="ec2-user"
export VM_IP="your-vm-ip-here"  # Replace with your actual VM IP
export VM_PATH="/home/ec2-user/autoblography_schandra/autoblography-main"

# Optional: SSH Key path (if not using default)
# export SSH_KEY_PATH="~/.ssh/your-key.pem"

# Optional: Custom SSH options
# export SSH_OPTS="-i $SSH_KEY_PATH -o StrictHostKeyChecking=no"

echo "VM Configuration loaded:"
echo "  User: $VM_USER"
echo "  IP: $VM_IP"
echo "  Path: $VM_PATH"
echo
echo "To use this configuration:"
echo "  source vm_config.sh"
echo "  ./deploy_to_vm.sh" 