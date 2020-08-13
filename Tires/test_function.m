% Author: Kat Chen
% Heavily referenced from: 
% https://www.mathworks.com/matlabcentral/fileexchange/67987-analyzing-tire-test-data

% For: http://www.fsaettc.org/data
% Only works with .mat files
% Output: matrix (nx2) with column 1 = FY,column 2 = SA

%% Initialization 
clear;
clc;
close all;

[file,path] = uigetfile("*.mat", "File Selector");
full_path = fullfile(path, file);
addpath(fullfile(pwd,'Functions'))

datamode = LongOrLat(); % You need to check if your files have longitudinal data
if( isa(file, 'double') && isequal(file, 0) )
    % No file was chosen, so we return
    return
else
    load(full_path)
end

% Functions for converting from lbf to N and psi to kPa
lbf2N = @(lbf)lbf*4.4482216152605;
N2lbf = @(N)N/4.4482216152605;

psi2kPa = @(psi)psi/0.145037737730217;
kPa2psi = @(kPa)kPa*0.145037737730217;

%% Binning Data

[FZ_binvals, P_binvals, IA_binvals] = Bin(FZ, P, IA);

errs = [35, 0.8, 0.2]; % tolerances for [FZ (lbf), Pressure (psi), IA (deg)]

FZ_bin = abs(FZ)>((FZ_binvals-errs(1))) & abs(FZ)<((FZ_binvals+errs(1))); % [lbf]
P_bin = P>(P_binvals-errs(2)) & P<(P_binvals+errs(2)); % [psi]
IA_bin = (IA>IA_binvals-errs(3)) & (IA<IA_binvals+errs(3)); % [deg]

if datamode == 1
    % Longitudinal data uses slip ratio
    S_0 = (-1<SL)&(SL<1);
else
    % Lateral data uses slip angles
    S_0 = (-1<SA)&(SA<1);
end

[IA_mat,FZ_mat] = meshgrid(IA_binvals,FZ_binvals);


