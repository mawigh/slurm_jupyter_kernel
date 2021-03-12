#!/usr/bin/python3

import argparse;
import json;
import pexpect;

# handle kernel as an object
class remoteslurmkernel:

    def __init__ (self, account, time, kernelcmd, partition="batch", cpus=None, memory=None, reservation=None):
        
        self.cpus = cpus;
        self.account = account;
        self.partition = partition;
        self.time = time;
        self.reservation = reservation;
        self.kernelcmd = kernelcmd;
        self.established = None;

        self.start_slurm_kernel();

    def start_slurm_kernel (self):

        cmd_args = [];
        default_slurm_job_name = 'jupyter_slurm_kernel';

        if not self.cpus == None:
            cmd_args.append(f'--cpus-per-task={cpus}');
        if not self.memory == None:
            cmd_args.append(f'--memory {memory}');
        if not self.reservation == None:
            cmd_args.append(f'--reservation {reservation}');

        cmd_args.append(f'--account={account}');
        cmd_args.append(f'--time={time}');
        cmd_args.append(f'--partition={partition}');

        cmd = f'srun {cmd_args} -J {default_slurm_kernel} -iv -u bash';
        
        self.slurm_session = pexpect.spawn(str(cmd), timeout=500);
       
        if not self.slurm_session == None:
            kernel_start = self.kernelcmd;
            self.slurm_session.sendline(kernel_start);

    def kernel_state ():
        while True:
            if not self.slurm_session.isalive():
                for logline in self.slurm_session.readlines():
                    if logline.strip():
                        print(str(logline));

def slurm_jupyter_kernel ():

    parser = argparse.ArgumentParser('Adding jupyter kernels using slurm');

    #parser.add_argument('connection_file', required=True);
    parser.add_argument('--cpus', help='slurm job spec: CPUs');
    parser.add_argument('--memory', help='slurm job spec: memory allocation');
    parser.add_argument('--time', required=True, help='slurm job spec: running time');
    parser.add_argument('--partition', help='slurm job spec: partition to use');
    parser.add_argument('--account', required=True, help='slurm job spec: account name');
    parser.add_argument('--reservation', help='reservation ID');
    parser.add_argument('--kernel-cmd', required=True, help='command to run jupyter kernel');

    args = parser.parse_args();

    obj_kernel = remoteslurmkernel(account=args.account,time=args.time, kernelcmd=args.kernel_cmd, partition=args.partition, cpus=args.cpus, memory=args.memory, reservation=args.reservation);

    obj_kernel.kernel_state();
