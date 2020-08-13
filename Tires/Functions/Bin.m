function [FZ_binvals, P_binvals, IA_binvals] = Bin(FZ, P, IA, ET)
%BIN 
% Bins FZ, P, and IA from the Calspan data and returns binning values
% (edges of bins).
% datamode - longitudinal(2) or lateral(2) data.
% If ET (elapsed time) is included, the variation plots will bes hown.

if exist("ET", "var")
    % Variation in FZ plot
    figure 
    plot(ET,FZ,'.'); 
    grid on 
    xlabel('Elapsed Time (s)'); 
    ylabel('FZ(lb)'); 
    title('Variation of FZ','FontSize',10);

    % Variation in Pressure plot
    figure 
    plot(ET,P); 
    xlabel('Elapsed Time (s)'); 
    ylabel('P (psi)'); 
    grid on
    title('Variation of Pressure','FontSize',10);

    % Variation in IA plot
    figure 
    plot(ET,IA); 
    xlabel('Elapsed Time (s)'); 
    ylabel('IA({\circ}''s)');
    grid on 
    title('Variation of IA','FontSize',10);
end

[countsFZ,edgesFZ] = histcounts(FZ);
[~,locsFZ] = findpeaks([countsFZ(2), countsFZ, countsFZ(end-1)]);
FZ_binvals = unique(round(abs(edgesFZ(locsFZ))/50) * 50); % round to nearest 50 pounds

[countsP,edgesP] = histcounts(P);
[~,locsP] = findpeaks([countsP(2), countsP, countsP(end-1)]);
P_binvals = unique(round(edgesP(locsP)));

[countsIA,edgesIA] = histcounts(IA);
[~,locsIA] = findpeaks([countsIA(2), countsIA, countsIA(end-1)]);
IA_binvals = unique(round(edgesIA(locsIA)));

if( isempty(FZ_binvals) || isempty(P_binvals) || isempty(IA_binvals) )
    error('One or more of the *_binValues arrays was empty.')
end

end

