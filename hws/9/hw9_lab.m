%%%%%%%%%%%%%% CS 70 Spring 2014 %%%%%%%%%%%%%%
%%% Solutions to Virtual Lab for Homework 9 %%%
%%%%%%%%%%%% Written by Ying Qiao %%%%%%%%%%%%%

set(0,'DefaultAxesFontSize', 14);
set(0,'DefaultTextFontSize', 14);


%%%%%%%%%%%%%%%%
%%% part (a) %%%
%%%%%%%%%%%%%%%%

p_vec = [0.9 0.6 0.5 0.4 0.3 0.1]; 
d_vec = linspace(-3,3,1000); 
M = 10000; colors = {'black','blue','red','green'}; 
k_vec = [10 100 1000 4000]; 
gaussian = @(x) exp(-x.^2/2)./sqrt(2.*pi);

for j = 1:length(p_vec)
    subplot(3,2,j); % plot setting for 6 p-values
    for i = 1:length(k_vec)
        coin = zeros(M,1); 
        S_k_normal = zeros(M,1); 
        for m = 1:M
            r = rand(k_vec(i),1); % k-by-1 array of rand in (0,1)
            coin(m,1) = sum(r <= p_vec(j)); % num of heads
            S_k_normal(m,1) = (coin(m,1)-k_vec(i)*p_vec(j))./sqrt(k_vec(i)*p_vec(j)*(1-p_vec(j))); % suggested S_k normalization
        end
        
        data = zeros(length(d_vec),1);        
        for a = 1:length(d_vec)
            data(a,1) = sum(S_k_normal < d_vec(a))./M; % fraction
        end
        
        plot(d_vec,data,'Color',colors{i},'LineWidth',3); % plot cdf
        hold on; 
    end   
    erf = zeros(length(d_vec),1);
    for a = 1:length(d_vec)
        erf(a,1) = integral(gaussian,-1000,d_vec(a)); % -inf as -1000
    end
    plot(d_vec,erf,'Color','magenta','LineWidth',2.5); % overlay erf
    
    h = legend('k = 10','k = 100','k = 1000','k = 4000', 'normal CDF','Location','NorthWest');
    set(h,'FontSize',6); 
    title(['p = ' num2str(p_vec(j)) ', m = ' num2str(M)]);
    xlabel('d'); ylabel('$P(\frac{S_k-kp}{\sqrt{k p (1-p)}} < d)$', 'interpreter','latex');
    set(gca,'XLim',[-3 3],'YLim',[0 1]);            
end
set(gcf,'PaperUnits','inches','PaperSize',[8,12],'PaperPosition',[0 0 8 12]);
print('-dpng','-r100','part_a');



%%%%%%%%%%%%%%%%
%%% part (c) %%%
%%%%%%%%%%%%%%%%

p_vec = [0.9 0.6 0.5 0.4 0.3 0.1]; 
d_vec = linspace(-3,3,1000); 
M = 10000; colors = {'black','blue','red','green'}; 
k_vec = [10 100 1000 4000]; 
gaussian = @(x) exp(-x.^2/2)./sqrt(2.*pi);

for j = 1:length(p_vec)
    for i = 1:length(k_vec)
        coin = zeros(M,1); 
        S_k_normal = zeros(M,1); 
        for m = 1:M
            r = rand(k_vec(i),1); % k-by-1 array of rand in (0,1)
            coin(m,1) = sum(r <= p_vec(j)); % num of heads
            S_k_normal(m,1) = (coin(m,1)-k_vec(i)*p_vec(j))./sqrt(k_vec(i)*p_vec(j)*(1-p_vec(j))); % suggested S_k normalization
        end
        
        bin_vec = linspace(-3,3,20); % has to adjust bin number for better plotting
        [N, cts] = hist(S_k_normal,bin_vec);
                
        subplot(3,2,j); % plot setting for 6 p-values
        ht = bar(cts, N/trapz(cts,N)); % normalize frequency to probability by area
        set(ht,'FaceColor','white','EdgeColor',colors{i},'LineWidth',2.5); 
        hold on;
    end   
    plot(d_vec, gaussian(d_vec), 'Color','magenta','LineWidth',2.5); %overlay pdf
    h = legend('k = 10','k = 100','k = 1000','k = 4000', 'normal PDF','Location','NorthWest');
    set(h,'FontSize',6); 
    title(['p = ' num2str(p_vec(j)) ', m = ' num2str(M)]);
    xlabel('$\frac{S_k-kp}{\sqrt{k p (1-p)}}$','interpreter','latex'); 
    ylabel('normalized frequency');
    set(gca,'XLim',[-3 3],'YLim',[0 0.6]);            
end
set(gcf,'PaperUnits','inches','PaperSize',[8,12],'PaperPosition',[0 0 8 12]);
print('-dpng','-r100','part_c');




%%%%%%%%%%%%%%%%
%%% part (d) %%%
%%%%%%%%%%%%%%%%

p_vec = [0.3 0.7]; 
a_del = [0.05 0.1]; 
k_vec = 10:200;
M = 10000; 
K = 200;
colors = {'black','blue','red','green'}; 
names = cell(4*3, 1); %dots, fitted lines, KL lines
KL_D = @(a,p) a*log(a/p)+(1-a)*log((1-a)/(1-p)); % K-L divergence

figure(1);
for j = 1:length(p_vec)
    p = p_vec(j);
    for i = 1:length(a_del)
        a = p+a_del(i);
        ind = (j-1)*2+i;
        names{ind*3-2} = ['p=' num2str(p) ', a=' num2str(a)];
        names{ind*3-1} = ['D(a||p)=' num2str(KL_D(a,p))];
                
        coin = zeros(M,K); 
        for m = 1:M
            for k = 10:K
                r = rand(k,1); % k-by-1 array of rand in (0,1)
                coin(m,k) = sum(r <= p); % num of heads
            end
        end
        
        S_k_frac = zeros(K,1); 
        for k = 10:K
            S_k_frac(k,1) = sum(coin(:,k) > k*a)/M; % quantile
        end
        
        data = log(S_k_frac(k_vec,1));
        lmod = polyfit(k_vec, data.', 1); % linear regression, dim match
        names{ind*3} = ['Slope=' num2str(lmod(1))];
        
        scatter(k_vec, data, 'MarkerEdgeColor',colors{ind}, 'LineWidth', 1); % dots
        hold on;
        plot(k_vec, k_vec*(-KL_D(a,p)), 'Color', colors{ind}, 'LineWidth', 1); % KL line
        plot(k_vec, polyval(lmod,k_vec), 'Color', colors{ind}, 'LineStyle', '-.', 'LineWidth', 3); % linear fit
        
        xlabel('k'); ylabel('$log(P(S_k > ak))$','interpreter','latex');
        set(gca,'XLim',[10 200],'YLim',[-5 0]);  
    end          
end

h = legend(names,'Location','SouthWest');
set(h,'FontSize',6); 

set(gcf,'PaperUnits','inches','PaperSize',[8,6],'PaperPosition',[0 0 8 6]);
print('-dpng','-r100','part_d');



%%%%%%%%%%%%%%%%
%%% part (e) %%%
%%%%%%%%%%%%%%%%

p_vec = [0.3 0.7]; 
eps = [0.1 0.2 0.3]; 
k_vec = 10:200;
M = 10000; 
K = 200;
colors = {'black','blue','green'}; 
names = cell(2*3, 1);

for j = 1:length(p_vec)
    p = p_vec(j);
    subplot(2,1,j);
    
    for i = 1:length(eps)
        e = eps(i);
        names{i*2-1} = ['trial frequency, e=' num2str(e)];
        names{i*2} = ['Chebyshev bound, e=' num2str(e)];
                
        coin = zeros(M,K); 
        for m = 1:M
            for k = 10:K
                r = rand(k,1); % k-by-1 array of rand in (0,1)
                coin(m,k) = sum(r <= p); % num of heads
            end
        end
        
        S_k_frac = zeros(K,1); 
        for k = 10:K
            S_k_frac(k,1) = sum(abs(coin(:,k)-k*p) >= e*k)/M; % quantile
        end
               
        plot(k_vec, S_k_frac(k_vec,1), 'Color', colors{i}, 'LineStyle', '-.', 'LineWidth', 3); % linear fit
        hold on;
        plot(k_vec, p*(1-p)./(e*e.*k_vec), 'Color', colors{i}, 'LineWidth', 1); % KL line     
    end
    xlabel('k'); ylabel('$P(|S_k-kp| \geq \epsilon k) \leq \frac{p(1-p)}{k\epsilon^2}$','interpreter','latex');
    set(gca,'XLim',[10 K],'YLim',[0 1]); 
    title(['p = ' num2str(p)]);
    h = legend(names,'Location','NorthEast');
    set(h,'FontSize',6);
end

set(gcf,'PaperUnits','inches','PaperSize',[6,8],'PaperPosition',[0 0 6 8]);
print('-dpng','-r100','part_e');



%%%%%%%%%%%%%%%%
%%% part (f) %%%
%%%%%%%%%%%%%%%%

n=50;
data = zeros(n,1);
for k = 1:n
    data(k,1) = nchoosek(n,k);
end

figure(2);
plot(1:n, data, 'b');
title('n=50');
xlabel('k'); ylabel('${n \choose k}$', 'interpreter','latex');

set(gcf,'PaperUnits','inches','PaperSize',[4,4],'PaperPosition',[0 0 4 4]);
print('-dpng','-r100','part_f');






