% AVL VSM Tire fits
clc
clear
close all;

% 250
Tire_250 = FY_SA_for_Load_psi_camber('B1654raw38.mat', -1100, 4, 85, 2);
[Tire_250_fit] = lsqcurvefit(@MagicFormula,[0.55 1.1],Tire_250(:,2),Tire_250(:,1),[],[]);
disp(Tire_250_fit);
times = linspace(-15,15, 100);

figure
hold on
plot(Tire_250(:,1), Tire_250(:,2),'ko');
plot(times,MagicFormula(Tire_250_fit,times),'b-');
hold off

%Tire_250_fit = tire_data_fit(Tire_250, 'poly3');
%sortrows(Tire_250_fit);
%plot(Tire_250(:,1), Tire_250(:,2))
xdata = - Tire_250(:,1);
Fx = Tire_250(:,2);
NormalLoad = 250;
save('Tire_250', 'Fx', 'NormalLoad', 'xdata');
hold on

% 200
Tire_200 = FY_SA_for_Load_psi_camber('B1654run24.mat', -889, 4, 85, 2);
%Tire_200_fit = tire_data_fit(Tire_200, 'poly3');
plot(Tire_200(:,1), Tire_200(:,2))
xdata = - Tire_200(:,1);
Fx = Tire_200(:,2);
NormalLoad = 200;
save('Tire_200', 'Fx', 'NormalLoad', 'xdata');

% 150
Tire_150 = FY_SA_for_Load_psi_camber('B1654run24.mat', -667, 4, 85, 2);
%Tire_150_fit = tire_data_fit(Tire_150, 'poly3');
plot(Tire_150(:,1), Tire_150(:,2))
xdata = - Tire_150(:,1);
Fx = Tire_150(:,2);
NormalLoad = 150;
save('Tire_150', 'Fx', 'NormalLoad', 'xdata');

% 100
Tire_100 = FY_SA_for_Load_psi_camber('B1654run24.mat', -444, 4, 85, 2);
%Tire_100_fit = tire_data_fit(Tire_100, 'poly3');
plot(Tire_100(:,1), Tire_100(:,2))
xdata = - Tire_100(:,1);
Fx = Tire_100(:,2);
NormalLoad = 100;
save('Tire_100', 'Fx', 'NormalLoad', 'xdata');

% 50
Tire_50 = FY_SA_for_Load_psi_camber('B1654run24.mat', -222, 4, 85, 2);
%Tire_50_fit = tire_data_fit(Tire_50, 'poly3');
plot(Tire_50(:,1), Tire_50(:,2))
xdata = - Tire_50(:,1);
Fx = Tire_50(:,2);
NormalLoad = 50;
save('Tire_50', 'Fx', 'NormalLoad', 'xdata');
ylabel('Fy (lbs)')
xlabel('SA (deg)')
legend('250lbs','200lbs','150lbs','100lbs', '50lbs')
hold off

function [F] = MagicFormula(Coeff,Slip)
%[F] = MagicFormula(Coeff,Slip)
%========================
%MAGIC FORMULA
%========================
%Magic formula function as per constraints defined in Patton (2013)
%=======================
%INPUT ARGUMENTS
%=======================
% Coeff = a 1x2 vector containing coefficients B and E
% Slip = Slip quantity (non-dimensional)
% constraints: C=1/B; D=1; You can adjust this Formula if necessary 
%=======================
%OUTPUT ARGUMENTS
%=======================
%F = non-dimensionalised force
%=======================
B = Coeff(1);
E = Coeff(2);
F = sin(1/B*atan(B*(1-E)*Slip+E*atan(B.*Slip)));
end