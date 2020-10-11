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

% for plotting surfaces, a meshgrid for normal force and IA bin values is created.
[IA_mat,FZ_mat] = meshgrid(IA_binvals,FZ_binvals);

% Preallocate memory for binning

A = cell(length(P_binvals),length(IA_binvals),length(FZ_binvals));

[S_binfzia, F_binfzia, NF_binfzia, ET_binfzia, FZ_binfzia, IA_binfzia, ...
    MX_binfzia, MZ_binfzia, CS_fzia, mu_fzia, S_H_fzia, S_V_fzia, S_bar_fzia, ...
    F_bar_fzia, B_fzia, C_fzia, D_fzia, E_fzia, F_M, S_M] = deal(A);

B = cell(length(P_binvals), 1);
[B_P, C_P, D_P, E_P, S_S_P, S_V_P, mu_P, S_H_P, CS_P, S_H_surf_IA_P, ...
    S_V_surf_IA_P, Mu_surf_IA_P, CS_surf_IA_P, B_surf_IA_P, C_surf_IA_P, ...
    D_surf_IA_P, E_surf_IA_P] = deal(B);

%% Data analysis by looping through pressure, FZ, then IA
for i=1:length(P_binvals)
    for k=1:size(FZ_bin,2)
        for j=1:size(IA_bin,2)
            validIdx = FZ_bin(:,k) & P_bin(:,i) & IA_bin(:,j) & S_0;
            ET_binfzia{i,j,k}  =  ET(validIdx);  % Time Bins
            FZ_binfzia{i,j,k}  =  FZ(validIdx);  % Vertical Load bins
            IA_binfzia{i,j,k}  =  IA(validIdx);  % Inclination Angle bins
            MX_binfzia{i,j,k}  =  MX(validIdx);  % Overturning Moment bins
            MZ_binfzia{i,j,k}  =  MZ(validIdx);  % Aligning Moment bins
            
            if datamode == 1
                F_binfzia{i,j,k}  =  FX(validIdx);  % Longitudinal Force Bins
                NF_binfzia{i,j,k} =  NFX(validIdx); % Force Coefficient bins
                S_binfzia{i,j,k}  =  SR(validIdx);  % Slip Ratio Bins
            else
                F_binfzia{i,j,k}  =  FY(validIdx);  % Lateral Force Bins
                NF_binfzia{i,j,k} =  NFY(validIdx); % Force Coefficient bins
                S_binfzia{i,j,k}  =  SA(validIdx);  % Slip Angle Bins
            end
            
            [CS_fzia{i,j,k}, mu_fzia{i,j,k}, S_H_fzia{i,j,k}, ...
             S_V_fzia{i,j,k}, S_bar_fzia{i,j,k}, F_bar_fzia{i,j,k}] = ...
                NonDimTrans( F_binfzia{i,j,k}, NF_binfzia{i,j,k}, ...
                    S_binfzia{i,j,k}, ET_binfzia{i,j,k}, FZ_binfzia{i,j,k}); 
            [B_fzia{i,j,k}, C_fzia{i,j,k}, D_fzia{i,j,k}, E_fzia{i,j,k}] = ...
                MagicFit(F_bar_fzia{i,j,k}, S_bar_fzia{i,j,k}); 
        end
    end
    
    B_P{i}   = permute(cell2mat(B_fzia(i,:,:)),[3,2,1])';
    C_P{i}   = permute(cell2mat(C_fzia(i,:,:)),[3,2,1])';
    D_P{i}   = permute(cell2mat(D_fzia(i,:,:)),[3,2,1])';
    E_P{i}   = permute(cell2mat(E_fzia(i,:,:)),[3,2,1])';
    S_S_P{i} = permute(cell2mat(CS_fzia(i,:,:)),[3,2,1])' ./FZ_binvals;
    S_V_P{i} = permute(cell2mat(S_V_fzia(i,:,:)),[3,2,1])'./FZ_binvals;
    mu_P{i}  = permute(cell2mat(mu_fzia(i,:,:)),[3,2,1])';
    S_H_P{i} = permute(cell2mat(S_H_fzia(i,:,:)),[3,2,1])'./FZ_binvals;
    CS_P{i}  = permute(cell2mat(CS_fzia(i,:,:)),[3,2,1])';
    
    x = IA_binvals;
    y = FZ_binvals;
    
    S_H_surf_IA_P{i} = ResponseSurf(S_H_P{i},y,x,2);
    S_V_surf_IA_P{i} = ResponseSurf(S_V_P{i},y,x,2);
    Mu_surf_IA_P{i}  = ResponseSurf(mu_P{i},y,x,2);
    CS_surf_IA_P{i}  = ResponseSurf(CS_P{i},y,x,2);
    B_surf_IA_P{i}   = ResponseSurf(B_P{i},y,x,2);
    C_surf_IA_P{i}   = ResponseSurf(C_P{i},y,x,2);
    D_surf_IA_P{i}   = ResponseSurf(D_P{i},y,x,2);
    E_surf_IA_P{i}   = ResponseSurf(E_P{i},y,x,2);
    
    Slip_fit = -3:0.01:3;
    
    for m=1:length(FZ_binvals)
        for n=1:length(IA_binvals)        
            [F_M{i,n,m},S_M{i,n,m}] = MagicOutput(MagicFormula([B_surf_IA_P{i}(IA_binvals(n),FZ_binvals(n)),...
                E_surf_IA_P{i}(IA_binvals(n),FZ_binvals(m))],Slip_fit),...
                Slip_fit,Mu_surf_IA_P{i}(IA_binvals(n),FZ_binvals(m)),...
                FZ_binvals(m),CS_surf_IA_P{i}(IA_binvals(n),FZ_binvals(m)),datamode);
            if(i==1)
                if(m==1 && n==1)
                    figure
                    ax1 = axes;
                    hold on
                    if datamode == 1
                        FvsS_Title = 'F_x vs. SR';
                        yLab = 'F_x (N)'; xLab = 'SR(-)';
                    else
                        FvsS_Title = 'F_y vs. SA';
                        yLab = 'F_y (N)'; xLab = 'SA(-)';
                    end
                    title(FvsS_Title);
                    xlabel(xLab);
                    ylabel(yLab);
                    grid on
                end
                if(n==1)
                    [Ft,SRt]= MagicOutput(F_bar_fzia{i,n,m},S_bar_fzia{i,n,m},...
                        Mu_surf_IA_P{i}(IA_binvals(n),FZ_binvals(m)),...
                        FZ_binvals(m),CS_surf_IA_P{i}(IA_binvals(n),FZ_binvals(m)),datamode);
                    
                    % Plotting the Line fit and the Raw Data Points
                        color = [(linspace(0,1,5))' (linspace(1,0,5))' ([0 .5 1 0.85 0])'];
                        % Matrix was created to have the same color betweeen data and fit line. Change the amount of values if more colors are needed.
                    plot(ax1,SRt,Ft,'.','Color',[color(m,1) (color(m,2)) color(m,3)],'HandleVisibility','off');
                    FZ_binvals_r = round(FZ_binvals,2);
                    plot(S_M{i,n,m}',F_M{i,n,m}','Color',[color(m,1) color(m,2) color(m,3)],'LineWidth',1,...
                        'DisplayName',[mat2str(FZ_binvals_r(m)) ' N']);  
                end     
            end
        end
    end
    
    % Creating the legend for figure. 
    h = legend(ax1,'show');
    set(h,'Location','eastoutside');
    htitle = get(h,'Title');
    set(htitle,'String','F_z (N)','FontSize',10);
    
 if(i==1)
        % Defining figures:
        [x_plot,y_plot] = meshgrid(0:0.25:4,linspace(FZ_binvals(1),FZ_binvals(end),11));      
        figure
            ax2 = axes;
            hold on
            grid on
            title('B vs. FZ vs. IA');
            xlabel('Inclination Angle ({\circ}''s)','Rotation',20);
            ylabel('F_Z (N)','Rotation',-30);
%             ylim([0 2000]); zlim([0 3.5]); % To make graph limits the same uncomment this line and edit values
            zlabel('B (-)');
            view([-37.5 30]);
        figure
            ax3 = axes;
            hold on
            grid on 
            title('C vs. FZ vs. IA');
            xlabel('Inclination Angle ({\circ}''s)');
            ylabel('F_Z (N)','FontSize',10,'Rotation',-30);
%             ylim([0 2000]); zlim([0 3.5]); % To make graph limits the same uncomment this line and edit values
            zlabel('C (-)');
            view([-37.5 30]);
% %  Ommitted due to assumption D = 1
%         figure
%             ax4 = axes;
%             hold on
%             grid on 
%             title('D vs. FZ vs. IA','FontSize',10);
%             xlabel('Inclination Angle ({\circ}''s)','Rotation',20);
%             ylabel('F_Z (N)','Rotation',-30);
%             ylim([0 2000]); zlim([0 3.5]); % To make graph limits the same uncomment this line and edit values
%             zlabel('D (-)','FontSize',10);
%             view([-37.5 30]);
        figure
            ax5 = axes;
            hold on
            grid on 
            title('E vs. FZ vs. IA','FontSize',10);
            xlabel('Inclination Angle ({\circ}''s)','FontSize',10,'Rotation',20);
            ylabel('F_Z (N)','Rotation',-30);
%             ylim([0 2000]); zlim([0 3.5]); % To make graph limits the same uncomment this line and edit values
            zlabel('E (-)');
            view([-37.5 30]);
    end
    
    plot3(ax2,IA_mat,FZ_mat,B_surf_IA_P{i}(IA_mat,FZ_mat),'.','MarkerSize',25,...
        'MarkerEdgeColor',[i==1 i==2 i==3],'HandleVisibility','off');
    mesh(ax2,x_plot,y_plot,(B_surf_IA_P{i}(x_plot,y_plot)),'EdgeColor','none','LineWidth',2,...
        'FaceAlpha',0.4,'FaceColor',[i==1 i==2 i==3],'DisplayName',[mat2str(P_binvals(i)) ' lbs']);
    plot3(ax3,IA_mat,FZ_mat,C_surf_IA_P{i}(IA_mat,FZ_mat),'.','MarkerSize',25,...
        'MarkerEdgeColor',[i==1 i==2 i==3],'HandleVisibility','off');
    mesh(ax3,x_plot,y_plot,(C_surf_IA_P{i}(x_plot,y_plot)),'EdgeColor','none','LineWidth',2,...
        'FaceAlpha',0.4,'FaceColor',[i==1 i==2 i==3],'DisplayName',[mat2str(P_binvals(i)) ' lbs']);
%     plot3(ax4,IA_mat,FZ_mat,D_surf_IA_P{i}(IA_mat,FZ_mat),'.','MarkerSize',25,...
%         'MarkerEdgeColor',[i==1 i==2 i==3],'HandleVisibility','off');
%     mesh(ax4,x_plot,y_plot,(D_surf_IA_P{i}(x_plot,y_plot)),'EdgeColor','none','LineWidth',2,...
%         'FaceAlpha',0.4,'FaceColor',[i==1 i==2 i==3],'DisplayName',[mat2str(P_binvals(i)) ' lbs']);
    plot3(ax5,IA_mat,FZ_mat,E_surf_IA_P{i}(IA_mat,FZ_mat),'.','MarkerSize',25,...
        'MarkerEdgeColor',[i==1 i==2 i==3],'HandleVisibility','off');
    mesh(ax5,x_plot,y_plot,(E_surf_IA_P{i}(x_plot,y_plot)),'EdgeColor','none','LineWidth',2,...
        'FaceAlpha',0.4,'FaceColor',[i==1 i==2 i==3],'DisplayName',[mat2str(P_binvals(i)) ' lbs']);
end
hLegend(1) = legend(ax2,'show');
hLegend(2) = legend(ax3,'show');
% hLegend(3) = legend(ax4,'show');
hLegend(4) = legend(ax5,'show');
    
    
           


